import datetime
import os
import signal
import sys
import warnings
from openai.validators import (
    write_out_file,
    apply_necessary_remediation,
    apply_optional_remediation,
    read_any_format,
    get_validators,
)

import openai


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def organization_info(obj):
    organization = getattr(obj, "organization", None)
    if organization is not None:
        return "[organization={}] ".format(organization)
    else:
        return ""


def display(obj):
    sys.stderr.write(organization_info(obj))
    sys.stderr.flush()
    print(obj)


def display_error(e):
    extra = (
        " (HTTP status code: {})".format(e.http_status)
        if e.http_status is not None
        else ""
    )
    sys.stderr.write(
        "{}{}Error:{} {}{}\n".format(
            organization_info(e), bcolors.FAIL, bcolors.ENDC, e, extra
        )
    )


class Engine:
    @classmethod
    def get(cls, args):
        engine = openai.Engine.retrieve(id=args.id)
        display(engine)

    @classmethod
    def update(cls, args):
        engine = openai.Engine(id=args.id)
        engine.replicas = args.replicas
        engine.save()
        display(engine)

    @classmethod
    def generate(cls, args):
        warnings.warn(
            "Engine.generate is deprecated, use Completion.create", DeprecationWarning
        )
        if args.completions and args.completions > 1 and args.stream:
            raise ValueError("Can't stream multiple completions with openai CLI")

        kwargs = {}
        if args.model is not None:
            kwargs["model"] = args.model
        resp = openai.Engine(id=args.id).generate(
            completions=args.completions,
            context=args.context,
            length=args.length,
            stream=args.stream,
            temperature=args.temperature,
            top_p=args.top_p,
            logprobs=args.logprobs,
            stop=args.stop,
            **kwargs,
        )
        if not args.stream:
            resp = [resp]

        for part in resp:
            completions = len(part["data"])
            for c_idx, c in enumerate(part["data"]):
                if completions > 1:
                    sys.stdout.write("===== Completion {} =====\n".format(c_idx))
                sys.stdout.write("".join(c["text"]))
                if completions > 1:
                    sys.stdout.write("\n")
                sys.stdout.flush()

    @classmethod
    def search(cls, args):
        # Will soon be deprecated and replaced by a Search.create
        params = {
            "query": args.query,
            "max_rerank": args.max_rerank,
            "return_metadata": args.return_metadata,
        }
        if args.documents:
            params["documents"] = args.documents
        if args.file:
            params["file"] = args.file

        resp = openai.Engine(id=args.id).search(**params)
        scores = [
            (search_result["score"], search_result["document"])
            for search_result in resp["data"]
        ]
        scores.sort(reverse=True)
        dataset = (
            args.documents if args.documents else [x["text"] for x in resp["data"]]
        )
        for score, document_idx in scores:
            print("=== score {:.3f} ===".format(score))
            print(dataset[document_idx])
            if (
                args.return_metadata
                and args.file
                and "metadata" in resp["data"][document_idx]
            ):
                print(f"METADATA: {resp['data'][document_idx]['metadata']}")

    @classmethod
    def list(cls, args):
        engines = openai.Engine.list()
        display(engines)


class Completion:
    @classmethod
    def create(cls, args):
        if args.n is not None and args.n > 1 and args.stream:
            raise ValueError("Can't stream completions with n>1 with the current CLI")

        if args.engine and args.model:
            warnings.warn(
                "In most cases, you should not be specifying both engine and model."
            )

        resp = openai.Completion.create(
            engine=args.engine,
            model=args.model,
            n=args.n,
            max_tokens=args.max_tokens,
            logprobs=args.logprobs,
            prompt=args.prompt,
            stream=args.stream,
            temperature=args.temperature,
            top_p=args.top_p,
            stop=args.stop,
            echo=True,
        )
        if not args.stream:
            resp = [resp]

        for part in resp:
            choices = part["choices"]
            for c_idx, c in enumerate(sorted(choices, key=lambda s: s["index"])):
                if len(choices) > 1:
                    sys.stdout.write("===== Completion {} =====\n".format(c_idx))
                sys.stdout.write(c["text"])
                if len(choices) > 1:
                    sys.stdout.write("\n")
                sys.stdout.flush()


class Model:
    @classmethod
    def get(cls, args):
        resp = openai.Model.retrieve(
            id=args.id,
        )
        print(resp)

    @classmethod
    def delete(cls, args):
        model = openai.Model(id=args.id).delete()
        print(model)

    @classmethod
    def list(cls, args):
        models = openai.Model.list()
        print(models)


class File:
    @classmethod
    def create(cls, args):
        resp = openai.File.create(
            file=open(args.file),
            purpose=args.purpose,
        )
        print(resp)

    @classmethod
    def get(cls, args):
        resp = openai.File.retrieve(id=args.id)
        print(resp)

    @classmethod
    def delete(cls, args):
        file = openai.File(id=args.id).delete()
        print(file)

    @classmethod
    def list(cls, args):
        file = openai.File.list()
        print(file)


class FineTune:
    @classmethod
    def list(cls, args):
        resp = openai.FineTune.list()
        print(resp)

    @classmethod
    def _get_or_upload(cls, file, check_if_file_exists=True):
        try:
            openai.File.retrieve(file)
        except openai.error.InvalidRequestError as e:
            if e.http_status == 404 and os.path.isfile(file):
                matching_files = openai.File.find_matching_files(
                    file=open(file), purpose="fine-tune"
                )
                if len(matching_files) > 0 and check_if_file_exists:
                    file_ids = [f["id"] for f in matching_files]
                    sys.stdout.write(
                        "Found potentially duplicated files with name '{name}', purpose 'fine-tune' and size {size} bytes\n".format(
                            name=matching_files[0]["filename"],
                            size=matching_files[0]["bytes"],
                        )
                    )
                    sys.stdout.write("\n".join(file_ids))
                    while True:
                        sys.stdout.write(
                            "\nEnter file ID to reuse an already uploaded file, or an empty string to upload this file anyway: "
                        )
                        inp = sys.stdin.readline().strip()
                        if inp in file_ids:
                            sys.stdout.write(
                                "Using your file {file}: {id}\n".format(
                                    file=file, id=inp
                                )
                            )
                            return inp
                        elif inp == "":
                            break
                        else:
                            sys.stdout.write(
                                "File id '{id}' is not among the IDs of the potentially duplicated files\n".format(
                                    id=inp
                                )
                            )

                resp = openai.File.create(
                    file=open(file),
                    purpose="fine-tune",
                )
                sys.stdout.write(
                    "Uploaded file from {file}: {id}\n".format(file=file, id=resp["id"])
                )
                return resp["id"]
        return file

    @classmethod
    def create(cls, args):
        create_args = {
            "training_file": cls._get_or_upload(
                args.training_file, args.check_if_files_exist
            ),
        }
        if args.validation_file:
            create_args["validation_file"] = cls._get_or_upload(
                args.validation_file, args.check_if_files_exist
            )

        for hparam in (
            "model",
            "n_epochs",
            "batch_size",
            "learning_rate_multiplier",
            "prompt_loss_weight",
            "use_packing",
            "compute_classification_metrics",
            "classification_n_classes",
            "classification_positive_class",
            "classification_betas",
        ):
            attr = getattr(args, hparam)
            if attr is not None:
                create_args[hparam] = attr

        resp = openai.FineTune.create(**create_args)

        if args.no_follow:
            print(resp)
            return

        sys.stdout.write(
            "Created fine-tune: {job_id}\n"
            "Streaming events until fine-tuning is complete...\n\n"
            "(Ctrl-C will interrupt the stream, but not cancel the fine-tune)\n".format(
                job_id=resp["id"]
            )
        )
        cls._stream_events(resp["id"])

    @classmethod
    def get(cls, args):
        resp = openai.FineTune.retrieve(id=args.id)
        print(resp)
        print(resp["result_files"][0])

    @classmethod
    def results(cls, args):
        fine_tune = openai.FineTune.retrieve(id=args.id)
        if "result_files" not in fine_tune or len(fine_tune["result_files"]) == 0:
            raise openai.error.InvalidRequestError(
                f"No results file available for fine-tune {args.id}", "id"
            )
        result_file = openai.FineTune.retrieve(id=args.id)["result_files"][0]
        resp = openai.File.download(id=result_file["id"])
        print(resp.decode("utf-8"))

    @classmethod
    def events(cls, args):
        if args.stream:
            raise openai.error.OpenAIError(
                message=(
                    "The --stream parameter is deprecated, use fine_tunes.follow "
                    "instead:\n\n"
                    "  openai api fine_tunes.follow -i {id}\n".format(id=args.id)
                ),
            )

        resp = openai.FineTune.list_events(id=args.id)  # type: ignore
        print(resp)

    @classmethod
    def follow(cls, args):
        cls._stream_events(args.id)

    @classmethod
    def _stream_events(cls, job_id):
        def signal_handler(sig, frame):
            status = openai.FineTune.retrieve(job_id).status
            sys.stdout.write(
                "\nStream interrupted. Job is still {status}.\n"
                "To resume the stream, run:\n\n"
                "  openai api fine_tunes.follow -i {job_id}\n\n"
                "To cancel your job, run:\n\n"
                "  openai api fine_tunes.cancel -i {job_id}\n\n".format(
                    status=status, job_id=job_id
                )
            )
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        events = openai.FineTune.stream_events(job_id)
        # TODO(rachel): Add a nifty spinner here.
        try:
            for event in events:
                sys.stdout.write(
                    "[%s] %s"
                    % (
                        datetime.datetime.fromtimestamp(event["created_at"]),
                        event["message"],
                    )
                )
                sys.stdout.write("\n")
                sys.stdout.flush()
        except Exception:
            sys.stdout.write(
                "\nStream interrupted (client disconnected).\n"
                "To resume the stream, run:\n\n"
                "  openai api fine_tunes.follow -i {job_id}\n\n".format(job_id=job_id)
            )
            return

        resp = openai.FineTune.retrieve(id=job_id)
        status = resp["status"]
        if status == "succeeded":
            sys.stdout.write("\nJob complete! Status: succeeded 🎉")
            sys.stdout.write(
                "\nTry out your fine-tuned model:\n\n"
                "openai api completions.create -m {model} -p <YOUR_PROMPT>".format(
                    model=resp["fine_tuned_model"]
                )
            )
        elif status == "failed":
            sys.stdout.write(
                "\nJob failed. Please contact support@openai.com if you need assistance."
            )
        sys.stdout.write("\n")

    @classmethod
    def cancel(cls, args):
        resp = openai.FineTune.cancel(id=args.id)
        print(resp)

    @classmethod
    def prepare_data(cls, args):

        sys.stdout.write("Analyzing...\n")
        fname = args.file
        df, remediation = read_any_format(fname)
        apply_necessary_remediation(None, remediation)

        validators = get_validators()

        optional_remediations = []
        if remediation is not None:
            optional_remediations.append(remediation)
        for validator in validators:
            remediation = validator(df)
            if remediation is not None:
                optional_remediations.append(remediation)
                df = apply_necessary_remediation(df, remediation)

        any_optional_or_necessary_remediations = any(
            [
                remediation
                for remediation in optional_remediations
                if remediation.optional_msg is not None
                or remediation.necessary_msg is not None
            ]
        )

        if any_optional_or_necessary_remediations:
            sys.stdout.write(
                "\n\nBased on the analysis we will perform the following actions:\n"
            )

            for remediation in optional_remediations:
                df = apply_optional_remediation(df, remediation)
        else:
            sys.stdout.write("\n\nNo remediations found.\n")

        write_out_file(df, fname, any_optional_or_necessary_remediations)


def tools_register(parser):
    subparsers = parser.add_subparsers(
        title="Tools", help="Convenience client side tools"
    )

    def help(args):
        parser.print_help()

    parser.set_defaults(func=help)

    sub = subparsers.add_parser("fine_tunes.prepare_data")
    sub.add_argument(
        "-f",
        "--file",
        required=True,
        help="JSONL, JSON, CSV, TSV, TXT or XLSX file containing prompt-completion examples to be analyzed."
        "This should be the local file path.",
    )
    sub.set_defaults(func=FineTune.prepare_data)


def api_register(parser):
    # Engine management
    subparsers = parser.add_subparsers(help="All API subcommands")

    def help(args):
        parser.print_help()

    parser.set_defaults(func=help)

    sub = subparsers.add_parser("engines.list")
    sub.set_defaults(func=Engine.list)

    sub = subparsers.add_parser("engines.get")
    sub.add_argument("-i", "--id", required=True)
    sub.set_defaults(func=Engine.get)

    sub = subparsers.add_parser("engines.update")
    sub.add_argument("-i", "--id", required=True)
    sub.add_argument("-r", "--replicas", type=int)
    sub.set_defaults(func=Engine.update)

    sub = subparsers.add_parser("engines.generate")
    sub.add_argument("-i", "--id", required=True)
    sub.add_argument(
        "--stream", help="Stream tokens as they're ready.", action="store_true"
    )
    sub.add_argument("-c", "--context", help="An optional context to generate from")
    sub.add_argument("-l", "--length", help="How many tokens to generate", type=int)
    sub.add_argument(
        "-t",
        "--temperature",
        help="""What sampling temperature to use. Higher values means the model will take more risks. Try 0.9 for more creative applications, and 0 (argmax sampling) for ones with a well-defined answer.

Mutually exclusive with `top_p`.""",
        type=float,
    )
    sub.add_argument(
        "-p",
        "--top_p",
        help="""An alternative to sampling with temperature, called nucleus sampling, where the considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10%% probability mass are considered.

            Mutually exclusive with `temperature`.""",
        type=float,
    )
    sub.add_argument(
        "-n",
        "--completions",
        help="How many parallel completions to run on this context",
        type=int,
    )
    sub.add_argument(
        "--logprobs",
        help="Include the log probabilites on the `logprobs` most likely tokens. So for example, if `logprobs` is 10, the API will return a list of the 10 most likely tokens. If `logprobs` is supplied, the API will always return the logprob of the generated token, so there may be up to `logprobs+1` elements in the response.",
        type=int,
    )
    sub.add_argument(
        "--stop", help="A stop sequence at which to stop generating tokens."
    )
    sub.add_argument(
        "-m",
        "--model",
        required=False,
        help="A model (most commonly a model ID) to generate from. Defaults to the engine's default model.",
    )
    sub.set_defaults(func=Engine.generate)

    sub = subparsers.add_parser("engines.search")
    sub.add_argument("-i", "--id", required=True)
    sub.add_argument(
        "-d",
        "--documents",
        action="append",
        help="List of documents to search over. Only one of `documents` or `file` may be supplied.",
        required=False,
    )
    sub.add_argument(
        "-f",
        "--file",
        help="A file id to search over.  Only one of `documents` or `file` may be supplied.",
        required=False,
    )
    sub.add_argument(
        "--max_rerank",
        help="The maximum number of documents to be re-ranked and returned by search. This flag only takes effect when `file` is set.",
        type=int,
        default=200,
    )
    sub.add_argument(
        "--return_metadata",
        help="A special boolean flag for showing metadata. If set `true`, each document entry in the returned json will contain a 'metadata' field. Default to be `false`. This flag only takes effect when `file` is set.",
        type=bool,
        default=False,
    )
    sub.add_argument("-q", "--query", required=True, help="Search query")
    sub.set_defaults(func=Engine.search)

    # Completions
    sub = subparsers.add_parser("completions.create")
    sub.add_argument(
        "-e",
        "--engine",
        help="The engine to use. See https://beta.openai.com/docs/engines for more about what engines are available.",
    )
    sub.add_argument(
        "-m",
        "--model",
        help="The model to use. At most one of `engine` or `model` should be specified.",
    )
    sub.add_argument(
        "--stream", help="Stream tokens as they're ready.", action="store_true"
    )
    sub.add_argument("-p", "--prompt", help="An optional prompt to complete from")
    sub.add_argument(
        "-M", "--max-tokens", help="The maximum number of tokens to generate", type=int
    )
    sub.add_argument(
        "-t",
        "--temperature",
        help="""What sampling temperature to use. Higher values means the model will take more risks. Try 0.9 for more creative applications, and 0 (argmax sampling) for ones with a well-defined answer.

Mutually exclusive with `top_p`.""",
        type=float,
    )
    sub.add_argument(
        "-P",
        "--top_p",
        help="""An alternative to sampling with temperature, called nucleus sampling, where the considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10%% probability mass are considered.

            Mutually exclusive with `temperature`.""",
        type=float,
    )
    sub.add_argument(
        "-n",
        "--n",
        help="How many sub-completions to generate for each prompt.",
        type=int,
    )
    sub.add_argument(
        "--logprobs",
        help="Include the log probabilites on the `logprobs` most likely tokens, as well the chosen tokens. So for example, if `logprobs` is 10, the API will return a list of the 10 most likely tokens. If `logprobs` is 0, only the chosen tokens will have logprobs returned.",
        type=int,
    )
    sub.add_argument(
        "--stop", help="A stop sequence at which to stop generating tokens."
    )
    sub.set_defaults(func=Completion.create)

    # Models
    sub = subparsers.add_parser("models.list")
    sub.set_defaults(func=Model.list)

    sub = subparsers.add_parser("models.get")
    sub.add_argument("-i", "--id", required=True, help="The model ID")
    sub.set_defaults(func=Model.get)

    sub = subparsers.add_parser("models.delete")
    sub.add_argument("-i", "--id", required=True, help="The model ID")
    sub.set_defaults(func=Model.delete)

    # Files
    sub = subparsers.add_parser("files.create")

    sub.add_argument(
        "-f",
        "--file",
        required=True,
        help="File to upload",
    )
    sub.add_argument(
        "-p",
        "--purpose",
        help="Why are you uploading this file? (see https://beta.openai.com/docs/api-reference/ for purposes)",
        required=True,
    )
    sub.set_defaults(func=File.create)

    sub = subparsers.add_parser("files.get")
    sub.add_argument("-i", "--id", required=True, help="The files ID")
    sub.set_defaults(func=File.get)

    sub = subparsers.add_parser("files.delete")
    sub.add_argument("-i", "--id", required=True, help="The files ID")
    sub.set_defaults(func=File.delete)

    sub = subparsers.add_parser("files.list")
    sub.set_defaults(func=File.list)

    # Finetune
    sub = subparsers.add_parser("fine_tunes.list")
    sub.set_defaults(func=FineTune.list)

    sub = subparsers.add_parser("fine_tunes.create")
    sub.add_argument(
        "-t",
        "--training_file",
        required=True,
        help="JSONL file containing prompt-completion examples for training. This can "
        "be the ID of a file uploaded through the OpenAI API (e.g. file-abcde12345) "
        "or a local file path.",
    )
    sub.add_argument(
        "-v",
        "--validation_file",
        help="JSONL file containing prompt-completion examples for validation. This can "
        "be the ID of a file uploaded through the OpenAI API (e.g. file-abcde12345) "
        "or a local file path.",
    )
    sub.add_argument(
        "--no_check_if_files_exist",
        dest="check_if_files_exist",
        action="store_false",
        help="If this argument is set and training_file or validation_file are file paths, immediately upload them. If this argument is not set, check if they may be duplicates of already uploaded files before uploading, based on file name and file size.",
    )
    sub.add_argument(
        "-m",
        "--model",
        help="The model to start fine-tuning from",
    )
    sub.add_argument(
        "--no_follow",
        action="store_true",
        help="If set, returns immediately after creating the job. Otherwise, streams events and waits for the job to complete.",
    )
    sub.add_argument(
        "--n_epochs",
        type=int,
        help="The number of epochs to train the model for. An epoch refers to one "
        "full cycle through the training dataset.",
    )
    sub.add_argument(
        "--batch_size",
        type=int,
        help="The batch size to use for training. The batch size is the number of "
        "training examples used to train a single forward and backward pass.",
    )
    sub.add_argument(
        "--learning_rate_multiplier",
        type=float,
        help="The learning rate multiplier to use for training. The fine-tuning "
        "learning rate is determined by the original learning rate used for "
        "pretraining multiplied by this value",
    )
    sub.add_argument(
        "--use_packing",
        action="store_true",
        dest="use_packing",
        help="On classification tasks, we recommend not setting this flag. "
        "On all other tasks, we recommend setting it. "
        "When set, we pack as many prompt-completion pairs as possible into each "
        "training example. This greatly increases the speed of a fine-tuning job, "
        "often without negatively affecting model performance.",
    )
    sub.add_argument(
        "--no_packing",
        action="store_false",
        dest="use_packing",
        help="Disables the packing flag (see --use_packing for description)",
    )
    sub.set_defaults(use_packing=None)
    sub.add_argument(
        "--prompt_loss_weight",
        type=float,
        help="The weight to use for the prompt loss. The optimum value here depends "
        "depends on your use case. This determines how much the model prioritizes "
        "learning from prompt tokens vs learning from completion tokens",
    )
    sub.add_argument(
        "--compute_classification_metrics",
        action="store_true",
        help="If set, we calculate classification-specific metrics such as accuracy "
        "and F-1 score using the validation set at the end of every epoch.",
    )
    sub.set_defaults(compute_classification_metrics=None)
    sub.add_argument(
        "--classification_n_classes",
        type=int,
        help="The number of classes in a classification task. This parameter is "
        "required for multiclass classification",
    )
    sub.add_argument(
        "--classification_positive_class",
        help="The positive class in binary classification. This parameter is needed "
        "to generate precision, recall and F-1 metrics when doing binary "
        "classification",
    )
    sub.add_argument(
        "--classification_betas",
        type=float,
        nargs="+",
        help="If this is provided, we calculate F-beta scores at the specified beta "
        "values. The F-beta score is a generalization of F-1 score. This is only "
        "used for binary classification.",
    )
    sub.set_defaults(func=FineTune.create)

    sub = subparsers.add_parser("fine_tunes.get")
    sub.add_argument("-i", "--id", required=True, help="The id of the fine-tune job")
    sub.set_defaults(func=FineTune.get)

    sub = subparsers.add_parser("fine_tunes.results")
    sub.add_argument("-i", "--id", required=True, help="The id of the fine-tune job")
    sub.set_defaults(func=FineTune.results)

    sub = subparsers.add_parser("fine_tunes.events")
    sub.add_argument("-i", "--id", required=True, help="The id of the fine-tune job")

    # TODO(rachel): Remove this in 1.0
    sub.add_argument(
        "-s",
        "--stream",
        action="store_true",
        help="[DEPRECATED] If set, events will be streamed until the job is done. Otherwise, "
        "displays the event history to date.",
    )
    sub.set_defaults(func=FineTune.events)

    sub = subparsers.add_parser("fine_tunes.follow")
    sub.add_argument("-i", "--id", required=True, help="The id of the fine-tune job")
    sub.set_defaults(func=FineTune.follow)

    sub = subparsers.add_parser("fine_tunes.cancel")
    sub.add_argument("-i", "--id", required=True, help="The id of the fine-tune job")
    sub.set_defaults(func=FineTune.cancel)
