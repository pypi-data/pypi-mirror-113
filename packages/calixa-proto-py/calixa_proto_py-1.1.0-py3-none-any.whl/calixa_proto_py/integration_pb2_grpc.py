# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import integration_pb2 as integration__pb2


class IntegrationServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.HealthCheck = channel.unary_unary(
                '/calixa.domain.integration.IntegrationService/HealthCheck',
                request_serializer=integration__pb2.HealthCheckRequest.SerializeToString,
                response_deserializer=integration__pb2.HealthCheckResponse.FromString,
                )
        self.Verify = channel.unary_unary(
                '/calixa.domain.integration.IntegrationService/Verify',
                request_serializer=integration__pb2.VerifyRequest.SerializeToString,
                response_deserializer=integration__pb2.VerifyResponse.FromString,
                )
        self.Install = channel.unary_unary(
                '/calixa.domain.integration.IntegrationService/Install',
                request_serializer=integration__pb2.InstallRequest.SerializeToString,
                response_deserializer=integration__pb2.InstallResponse.FromString,
                )
        self.Uninstall = channel.unary_unary(
                '/calixa.domain.integration.IntegrationService/Uninstall',
                request_serializer=integration__pb2.UninstallRequest.SerializeToString,
                response_deserializer=integration__pb2.UninstallResponse.FromString,
                )
        self.InitializeBackfill = channel.unary_unary(
                '/calixa.domain.integration.IntegrationService/InitializeBackfill',
                request_serializer=integration__pb2.InitializeBackfillRequest.SerializeToString,
                response_deserializer=integration__pb2.InitializeBackfillResponse.FromString,
                )
        self.BackfillPartial = channel.unary_unary(
                '/calixa.domain.integration.IntegrationService/BackfillPartial',
                request_serializer=integration__pb2.BackfillPartialRequest.SerializeToString,
                response_deserializer=integration__pb2.BackfillPartialResponse.FromString,
                )
        self.ProcessLogEntry = channel.unary_unary(
                '/calixa.domain.integration.IntegrationService/ProcessLogEntry',
                request_serializer=integration__pb2.ProcessLogEntryRequest.SerializeToString,
                response_deserializer=integration__pb2.ProcessLogEntryResponse.FromString,
                )
        self.GetOAuthAuthenticationUrl = channel.unary_unary(
                '/calixa.domain.integration.IntegrationService/GetOAuthAuthenticationUrl',
                request_serializer=integration__pb2.OAuthAuthenticationUrlRequest.SerializeToString,
                response_deserializer=integration__pb2.OAuthAuthenticationUrlResponse.FromString,
                )
        self.FinalizeOAuthIntegration = channel.unary_unary(
                '/calixa.domain.integration.IntegrationService/FinalizeOAuthIntegration',
                request_serializer=integration__pb2.FinalizeOAuthIntegrationRequest.SerializeToString,
                response_deserializer=integration__pb2.FinalizeOAuthIntegrationResponse.FromString,
                )
        self.InvokeAction = channel.unary_unary(
                '/calixa.domain.integration.IntegrationService/InvokeAction',
                request_serializer=integration__pb2.InvokeIntegrationActionRequest.SerializeToString,
                response_deserializer=integration__pb2.InvokeIntegrationActionResponse.FromString,
                )
        self.GetRelatedData = channel.unary_unary(
                '/calixa.domain.integration.IntegrationService/GetRelatedData',
                request_serializer=integration__pb2.GetIntegrationRelatedDataRequest.SerializeToString,
                response_deserializer=integration__pb2.GetIntegrationRelatedDataResponse.FromString,
                )


class IntegrationServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def HealthCheck(self, request, context):
        """HealthCheck can be called periodically by the Platform to ensure that an integration
        is doing well.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Verify(self, request, context):
        """Verifies that the credentials (parameters, config, etc) for an integration is correct
        and ready for an install and on-going webhooks/incremental updates and backfill.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Install(self, request, context):
        """Performs a full install (this is different than verifying that credentials work) of
        the integration for the Organization (and InstanceID).
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Uninstall(self, request, context):
        """Performs a complete uninstall of the integration from 3rd party apps. Steps could include
        - Revoke access token
        - Remove configured webhooks settings
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def InitializeBackfill(self, request, context):
        """For more detailed workflow description, refer https://www.notion.so/Backfill-2-0-357737f0ba0a49ac97aa0074fe9878e1#fddaa33ff74d4351b5fb602aacc31d0c

        InitializeBackfill is called by the platform to fetch the initial set of BackfillTask's
        required to start the backfill per entity_type. Current limit for the number of initial set of tasks is ten.

        The BackfillTask contains information, like time_range, page_cursor, to perform smallest unit of backfill work.
        For example:
        backfill_page : {page: 1, per_page: 20, starting_after='page_cursor1'},
        backfill_time_range: {from_at: 1621238411, to_at: 1621299611}

        The platform saves the tasks to a postgres table for observability and status tracking,
        and publishes the tasks to a pub/sub topic to be reliably delivered to the integrations for backfill.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BackfillPartial(self, request, context):
        """For more detailed workflow description, refer https://www.notion.so/Backfill-2-0-357737f0ba0a49ac97aa0074fe9878e1#fddaa33ff74d4351b5fb602aacc31d0c

        BackfillPartial is long running, slow, susceptible to errors from 3rd party api's and save entities to platform operations.
        BackfillPartial is called by the platform, in a fire-and-forget manner, for each published BackfillTask, and it is responsible for the following
        1. (slow, error prone) Fetches the data from 3rd party using the information, like backfill_page, backfill_time_range, present in BackfillTask.
        2. (slow, error prone) Converts the fetched raw data into calixa entities and save each entity in graph by calling platform.
        3. Updates the status of the BackfillTask in postgres table to reflect the true state of the operation by calling platform.
        4. If the current BackfillTask status is success and more results needs to be processed from 3rd party,
        a new BackfillTask to fetch the next results is enqueued by calling platform.
        5. If the current BackfillTask failed, the status is updated in the platform, errors sent to sentry, prometheus and backfill exits.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ProcessLogEntry(self, request, context):
        """Called by the platform after a log entry for the integration has been
        durably written.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetOAuthAuthenticationUrl(self, request, context):
        """Called by the IntegrationManager when a user tries to install an integration. This RPC
        must return the URL that the browser is redirected to initiate the OAuth flow.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FinalizeOAuthIntegration(self, request, context):
        """This RPC is called when the final step in the OAuth flow completes. The RPC must fetch
        the access token (and other OAuth properties) from the third-party and return the OAuthCredentials
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def InvokeAction(self, request, context):
        """Called by ActionService to invoke action(s) on the 3rd party connected integration vendors like
        Stripe, Intercom, Hubspot, Zendesk etc. Examples of action's could be
        1) (Stripe)   mark the invoice as paid, refund, etc.
        2) (Hubspot)  close the deal
        3) (Intercom) send a follow up message
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetRelatedData(self, request, context):
        """Fetches information that is not captured by entities inside Calixa or information
        that needs a real time lookup, e.g.: Stripe Coupon
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_IntegrationServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'HealthCheck': grpc.unary_unary_rpc_method_handler(
                    servicer.HealthCheck,
                    request_deserializer=integration__pb2.HealthCheckRequest.FromString,
                    response_serializer=integration__pb2.HealthCheckResponse.SerializeToString,
            ),
            'Verify': grpc.unary_unary_rpc_method_handler(
                    servicer.Verify,
                    request_deserializer=integration__pb2.VerifyRequest.FromString,
                    response_serializer=integration__pb2.VerifyResponse.SerializeToString,
            ),
            'Install': grpc.unary_unary_rpc_method_handler(
                    servicer.Install,
                    request_deserializer=integration__pb2.InstallRequest.FromString,
                    response_serializer=integration__pb2.InstallResponse.SerializeToString,
            ),
            'Uninstall': grpc.unary_unary_rpc_method_handler(
                    servicer.Uninstall,
                    request_deserializer=integration__pb2.UninstallRequest.FromString,
                    response_serializer=integration__pb2.UninstallResponse.SerializeToString,
            ),
            'InitializeBackfill': grpc.unary_unary_rpc_method_handler(
                    servicer.InitializeBackfill,
                    request_deserializer=integration__pb2.InitializeBackfillRequest.FromString,
                    response_serializer=integration__pb2.InitializeBackfillResponse.SerializeToString,
            ),
            'BackfillPartial': grpc.unary_unary_rpc_method_handler(
                    servicer.BackfillPartial,
                    request_deserializer=integration__pb2.BackfillPartialRequest.FromString,
                    response_serializer=integration__pb2.BackfillPartialResponse.SerializeToString,
            ),
            'ProcessLogEntry': grpc.unary_unary_rpc_method_handler(
                    servicer.ProcessLogEntry,
                    request_deserializer=integration__pb2.ProcessLogEntryRequest.FromString,
                    response_serializer=integration__pb2.ProcessLogEntryResponse.SerializeToString,
            ),
            'GetOAuthAuthenticationUrl': grpc.unary_unary_rpc_method_handler(
                    servicer.GetOAuthAuthenticationUrl,
                    request_deserializer=integration__pb2.OAuthAuthenticationUrlRequest.FromString,
                    response_serializer=integration__pb2.OAuthAuthenticationUrlResponse.SerializeToString,
            ),
            'FinalizeOAuthIntegration': grpc.unary_unary_rpc_method_handler(
                    servicer.FinalizeOAuthIntegration,
                    request_deserializer=integration__pb2.FinalizeOAuthIntegrationRequest.FromString,
                    response_serializer=integration__pb2.FinalizeOAuthIntegrationResponse.SerializeToString,
            ),
            'InvokeAction': grpc.unary_unary_rpc_method_handler(
                    servicer.InvokeAction,
                    request_deserializer=integration__pb2.InvokeIntegrationActionRequest.FromString,
                    response_serializer=integration__pb2.InvokeIntegrationActionResponse.SerializeToString,
            ),
            'GetRelatedData': grpc.unary_unary_rpc_method_handler(
                    servicer.GetRelatedData,
                    request_deserializer=integration__pb2.GetIntegrationRelatedDataRequest.FromString,
                    response_serializer=integration__pb2.GetIntegrationRelatedDataResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'calixa.domain.integration.IntegrationService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class IntegrationService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def HealthCheck(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.integration.IntegrationService/HealthCheck',
            integration__pb2.HealthCheckRequest.SerializeToString,
            integration__pb2.HealthCheckResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Verify(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.integration.IntegrationService/Verify',
            integration__pb2.VerifyRequest.SerializeToString,
            integration__pb2.VerifyResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Install(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.integration.IntegrationService/Install',
            integration__pb2.InstallRequest.SerializeToString,
            integration__pb2.InstallResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Uninstall(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.integration.IntegrationService/Uninstall',
            integration__pb2.UninstallRequest.SerializeToString,
            integration__pb2.UninstallResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def InitializeBackfill(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.integration.IntegrationService/InitializeBackfill',
            integration__pb2.InitializeBackfillRequest.SerializeToString,
            integration__pb2.InitializeBackfillResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BackfillPartial(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.integration.IntegrationService/BackfillPartial',
            integration__pb2.BackfillPartialRequest.SerializeToString,
            integration__pb2.BackfillPartialResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ProcessLogEntry(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.integration.IntegrationService/ProcessLogEntry',
            integration__pb2.ProcessLogEntryRequest.SerializeToString,
            integration__pb2.ProcessLogEntryResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetOAuthAuthenticationUrl(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.integration.IntegrationService/GetOAuthAuthenticationUrl',
            integration__pb2.OAuthAuthenticationUrlRequest.SerializeToString,
            integration__pb2.OAuthAuthenticationUrlResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def FinalizeOAuthIntegration(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.integration.IntegrationService/FinalizeOAuthIntegration',
            integration__pb2.FinalizeOAuthIntegrationRequest.SerializeToString,
            integration__pb2.FinalizeOAuthIntegrationResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def InvokeAction(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.integration.IntegrationService/InvokeAction',
            integration__pb2.InvokeIntegrationActionRequest.SerializeToString,
            integration__pb2.InvokeIntegrationActionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetRelatedData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.integration.IntegrationService/GetRelatedData',
            integration__pb2.GetIntegrationRelatedDataRequest.SerializeToString,
            integration__pb2.GetIntegrationRelatedDataResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
