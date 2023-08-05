"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import authzed.api.v0.core_pb2
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor = ...

class UpgradeSchemaRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    NAMESPACE_CONFIGS_FIELD_NUMBER: builtins.int

    @property
    def namespace_configs(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]: ...

    def __init__(self,
        *,
        namespace_configs : typing.Optional[typing.Iterable[typing.Text]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"namespace_configs",b"namespace_configs"]) -> None: ...
global___UpgradeSchemaRequest = UpgradeSchemaRequest

class UpgradeSchemaResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    ERROR_FIELD_NUMBER: builtins.int
    UPGRADED_SCHEMA_FIELD_NUMBER: builtins.int
    upgraded_schema: typing.Text = ...

    @property
    def error(self) -> global___DeveloperError: ...

    def __init__(self,
        *,
        error : typing.Optional[global___DeveloperError] = ...,
        upgraded_schema : typing.Text = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal[u"error",b"error"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"error",b"error",u"upgraded_schema",b"upgraded_schema"]) -> None: ...
global___UpgradeSchemaResponse = UpgradeSchemaResponse

class ShareRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    SCHEMA_FIELD_NUMBER: builtins.int
    RELATIONSHIPS_YAML_FIELD_NUMBER: builtins.int
    VALIDATION_YAML_FIELD_NUMBER: builtins.int
    ASSERTIONS_YAML_FIELD_NUMBER: builtins.int
    schema: typing.Text = ...
    relationships_yaml: typing.Text = ...
    validation_yaml: typing.Text = ...
    assertions_yaml: typing.Text = ...

    def __init__(self,
        *,
        schema : typing.Text = ...,
        relationships_yaml : typing.Text = ...,
        validation_yaml : typing.Text = ...,
        assertions_yaml : typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"assertions_yaml",b"assertions_yaml",u"relationships_yaml",b"relationships_yaml",u"schema",b"schema",u"validation_yaml",b"validation_yaml"]) -> None: ...
global___ShareRequest = ShareRequest

class ShareResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    SHARE_REFERENCE_FIELD_NUMBER: builtins.int
    share_reference: typing.Text = ...

    def __init__(self,
        *,
        share_reference : typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"share_reference",b"share_reference"]) -> None: ...
global___ShareResponse = ShareResponse

class LookupShareRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    SHARE_REFERENCE_FIELD_NUMBER: builtins.int
    share_reference: typing.Text = ...

    def __init__(self,
        *,
        share_reference : typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"share_reference",b"share_reference"]) -> None: ...
global___LookupShareRequest = LookupShareRequest

class LookupShareResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    class LookupStatus(metaclass=_LookupStatus):
        V = typing.NewType('V', builtins.int)

    UNKNOWN_REFERENCE = LookupShareResponse.LookupStatus.V(0)
    FAILED_TO_LOOKUP = LookupShareResponse.LookupStatus.V(1)
    VALID_REFERENCE = LookupShareResponse.LookupStatus.V(2)
    UPGRADED_REFERENCE = LookupShareResponse.LookupStatus.V(3)

    class _LookupStatus(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[LookupStatus.V], builtins.type):  # type: ignore
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor = ...
        UNKNOWN_REFERENCE = LookupShareResponse.LookupStatus.V(0)
        FAILED_TO_LOOKUP = LookupShareResponse.LookupStatus.V(1)
        VALID_REFERENCE = LookupShareResponse.LookupStatus.V(2)
        UPGRADED_REFERENCE = LookupShareResponse.LookupStatus.V(3)

    STATUS_FIELD_NUMBER: builtins.int
    SCHEMA_FIELD_NUMBER: builtins.int
    RELATIONSHIPS_YAML_FIELD_NUMBER: builtins.int
    VALIDATION_YAML_FIELD_NUMBER: builtins.int
    ASSERTIONS_YAML_FIELD_NUMBER: builtins.int
    status: global___LookupShareResponse.LookupStatus.V = ...
    schema: typing.Text = ...
    relationships_yaml: typing.Text = ...
    validation_yaml: typing.Text = ...
    assertions_yaml: typing.Text = ...

    def __init__(self,
        *,
        status : global___LookupShareResponse.LookupStatus.V = ...,
        schema : typing.Text = ...,
        relationships_yaml : typing.Text = ...,
        validation_yaml : typing.Text = ...,
        assertions_yaml : typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"assertions_yaml",b"assertions_yaml",u"relationships_yaml",b"relationships_yaml",u"schema",b"schema",u"status",b"status",u"validation_yaml",b"validation_yaml"]) -> None: ...
global___LookupShareResponse = LookupShareResponse

class RequestContext(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    SCHEMA_FIELD_NUMBER: builtins.int
    RELATIONSHIPS_FIELD_NUMBER: builtins.int
    schema: typing.Text = ...

    @property
    def relationships(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[authzed.api.v0.core_pb2.RelationTuple]: ...

    def __init__(self,
        *,
        schema : typing.Text = ...,
        relationships : typing.Optional[typing.Iterable[authzed.api.v0.core_pb2.RelationTuple]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"relationships",b"relationships",u"schema",b"schema"]) -> None: ...
global___RequestContext = RequestContext

class EditCheckRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    CONTEXT_FIELD_NUMBER: builtins.int
    CHECK_RELATIONSHIPS_FIELD_NUMBER: builtins.int

    @property
    def context(self) -> global___RequestContext: ...

    @property
    def check_relationships(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[authzed.api.v0.core_pb2.RelationTuple]: ...

    def __init__(self,
        *,
        context : typing.Optional[global___RequestContext] = ...,
        check_relationships : typing.Optional[typing.Iterable[authzed.api.v0.core_pb2.RelationTuple]] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal[u"context",b"context"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"check_relationships",b"check_relationships",u"context",b"context"]) -> None: ...
global___EditCheckRequest = EditCheckRequest

class EditCheckResult(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    RELATIONSHIP_FIELD_NUMBER: builtins.int
    IS_MEMBER_FIELD_NUMBER: builtins.int
    ERROR_FIELD_NUMBER: builtins.int
    is_member: builtins.bool = ...

    @property
    def relationship(self) -> authzed.api.v0.core_pb2.RelationTuple: ...

    @property
    def error(self) -> global___DeveloperError: ...

    def __init__(self,
        *,
        relationship : typing.Optional[authzed.api.v0.core_pb2.RelationTuple] = ...,
        is_member : builtins.bool = ...,
        error : typing.Optional[global___DeveloperError] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal[u"error",b"error",u"relationship",b"relationship"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"error",b"error",u"is_member",b"is_member",u"relationship",b"relationship"]) -> None: ...
global___EditCheckResult = EditCheckResult

class EditCheckResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    REQUEST_ERRORS_FIELD_NUMBER: builtins.int
    CHECK_RESULTS_FIELD_NUMBER: builtins.int

    @property
    def request_errors(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___DeveloperError]: ...

    @property
    def check_results(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___EditCheckResult]: ...

    def __init__(self,
        *,
        request_errors : typing.Optional[typing.Iterable[global___DeveloperError]] = ...,
        check_results : typing.Optional[typing.Iterable[global___EditCheckResult]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"check_results",b"check_results",u"request_errors",b"request_errors"]) -> None: ...
global___EditCheckResponse = EditCheckResponse

class ValidateRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    CONTEXT_FIELD_NUMBER: builtins.int
    VALIDATION_YAML_FIELD_NUMBER: builtins.int
    UPDATE_VALIDATION_YAML_FIELD_NUMBER: builtins.int
    ASSERTIONS_YAML_FIELD_NUMBER: builtins.int
    validation_yaml: typing.Text = ...
    update_validation_yaml: builtins.bool = ...
    assertions_yaml: typing.Text = ...

    @property
    def context(self) -> global___RequestContext: ...

    def __init__(self,
        *,
        context : typing.Optional[global___RequestContext] = ...,
        validation_yaml : typing.Text = ...,
        update_validation_yaml : builtins.bool = ...,
        assertions_yaml : typing.Text = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal[u"context",b"context"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"assertions_yaml",b"assertions_yaml",u"context",b"context",u"update_validation_yaml",b"update_validation_yaml",u"validation_yaml",b"validation_yaml"]) -> None: ...
global___ValidateRequest = ValidateRequest

class ValidateResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    REQUEST_ERRORS_FIELD_NUMBER: builtins.int
    VALIDATION_ERRORS_FIELD_NUMBER: builtins.int
    UPDATED_VALIDATION_YAML_FIELD_NUMBER: builtins.int
    updated_validation_yaml: typing.Text = ...

    @property
    def request_errors(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___DeveloperError]: ...

    @property
    def validation_errors(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___DeveloperError]: ...

    def __init__(self,
        *,
        request_errors : typing.Optional[typing.Iterable[global___DeveloperError]] = ...,
        validation_errors : typing.Optional[typing.Iterable[global___DeveloperError]] = ...,
        updated_validation_yaml : typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"request_errors",b"request_errors",u"updated_validation_yaml",b"updated_validation_yaml",u"validation_errors",b"validation_errors"]) -> None: ...
global___ValidateResponse = ValidateResponse

class DeveloperError(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    class Source(metaclass=_Source):
        V = typing.NewType('V', builtins.int)

    UNKNOWN_SOURCE = DeveloperError.Source.V(0)
    SCHEMA = DeveloperError.Source.V(1)
    RELATIONSHIP = DeveloperError.Source.V(2)
    VALIDATION_YAML = DeveloperError.Source.V(3)
    CHECK_WATCH = DeveloperError.Source.V(4)
    ASSERTION = DeveloperError.Source.V(5)

    class _Source(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[Source.V], builtins.type):  # type: ignore
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor = ...
        UNKNOWN_SOURCE = DeveloperError.Source.V(0)
        SCHEMA = DeveloperError.Source.V(1)
        RELATIONSHIP = DeveloperError.Source.V(2)
        VALIDATION_YAML = DeveloperError.Source.V(3)
        CHECK_WATCH = DeveloperError.Source.V(4)
        ASSERTION = DeveloperError.Source.V(5)

    class ErrorKind(metaclass=_ErrorKind):
        V = typing.NewType('V', builtins.int)

    UNKNOWN_KIND = DeveloperError.ErrorKind.V(0)
    PARSE_ERROR = DeveloperError.ErrorKind.V(1)
    SCHEMA_ISSUE = DeveloperError.ErrorKind.V(2)
    DUPLICATE_RELATIONSHIP = DeveloperError.ErrorKind.V(3)
    MISSING_EXPECTED_RELATIONSHIP = DeveloperError.ErrorKind.V(4)
    EXTRA_RELATIONSHIP_FOUND = DeveloperError.ErrorKind.V(5)
    UNKNOWN_OBJECT_TYPE = DeveloperError.ErrorKind.V(6)
    UNKNOWN_RELATION = DeveloperError.ErrorKind.V(7)
    MAXIMUM_RECURSION = DeveloperError.ErrorKind.V(8)
    ASSERTION_FAILED = DeveloperError.ErrorKind.V(9)

    class _ErrorKind(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[ErrorKind.V], builtins.type):  # type: ignore
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor = ...
        UNKNOWN_KIND = DeveloperError.ErrorKind.V(0)
        PARSE_ERROR = DeveloperError.ErrorKind.V(1)
        SCHEMA_ISSUE = DeveloperError.ErrorKind.V(2)
        DUPLICATE_RELATIONSHIP = DeveloperError.ErrorKind.V(3)
        MISSING_EXPECTED_RELATIONSHIP = DeveloperError.ErrorKind.V(4)
        EXTRA_RELATIONSHIP_FOUND = DeveloperError.ErrorKind.V(5)
        UNKNOWN_OBJECT_TYPE = DeveloperError.ErrorKind.V(6)
        UNKNOWN_RELATION = DeveloperError.ErrorKind.V(7)
        MAXIMUM_RECURSION = DeveloperError.ErrorKind.V(8)
        ASSERTION_FAILED = DeveloperError.ErrorKind.V(9)

    MESSAGE_FIELD_NUMBER: builtins.int
    LINE_FIELD_NUMBER: builtins.int
    COLUMN_FIELD_NUMBER: builtins.int
    SOURCE_FIELD_NUMBER: builtins.int
    KIND_FIELD_NUMBER: builtins.int
    PATH_FIELD_NUMBER: builtins.int
    CONTEXT_FIELD_NUMBER: builtins.int
    message: typing.Text = ...
    line: builtins.int = ...
    column: builtins.int = ...
    source: global___DeveloperError.Source.V = ...
    kind: global___DeveloperError.ErrorKind.V = ...

    @property
    def path(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]: ...
    context: typing.Text = ...

    def __init__(self,
        *,
        message : typing.Text = ...,
        line : builtins.int = ...,
        column : builtins.int = ...,
        source : global___DeveloperError.Source.V = ...,
        kind : global___DeveloperError.ErrorKind.V = ...,
        path : typing.Optional[typing.Iterable[typing.Text]] = ...,
        context : typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"column",b"column",u"context",b"context",u"kind",b"kind",u"line",b"line",u"message",b"message",u"path",b"path",u"source",b"source"]) -> None: ...
global___DeveloperError = DeveloperError
