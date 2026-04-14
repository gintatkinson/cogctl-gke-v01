//     NEC Laboratories Europe GmbH
//
//     PROPRIETARY INFORMATION
//
// The software and its source code contain valuable trade secrets and
// shall be maintained in confidence and treated as confidential
// information. The software may only be used for evaluation and/or
// testing purposes, unless otherwise explicitly stated in a written
// agreement with NEC Laboratories Europe GmbH.
//
// Any unauthorized publication, transfer to third parties or
// duplication of the object or source code - either totally or in
// part - is strictly prohibited.
//
//          Copyright (c) 2022 NEC Laboratories Europe GmbH
//          All Rights Reserved.
//
// Authors: Konstantin Munichev <konstantin.munichev@neclab.eu>
//
//
// NEC Laboratories Europe GmbH DISCLAIMS ALL WARRANTIES, EITHER
// EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO IMPLIED WARRANTIES
// OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE AND THE
// WARRANTY AGAINST LATENT DEFECTS, WITH RESPECT TO THE PROGRAM AND
// THE ACCOMPANYING DOCUMENTATION.
//
// NO LIABILITIES FOR CONSEQUENTIAL DAMAGES: IN NO EVENT SHALL NEC
// Laboratories Europe GmbH or ANY OF ITS SUBSIDIARIES BE LIABLE FOR
// ANY DAMAGES WHATSOEVER (INCLUDING, WITHOUT LIMITATION, DAMAGES FOR
// LOSS OF BUSINESS PROFITS, BUSINESS INTERRUPTION, LOSS OF
// INFORMATION, OR OTHER PECUNIARY LOSS AND INDIRECT, CONSEQUENTIAL,
// INCIDENTAL, ECONOMIC OR PUNITIVE DAMAGES) ARISING OUT OF THE USE OF
// OR INABILITY TO USE THIS PROGRAM, EVEN IF NEC Laboratories Europe
// GmbH HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
//
// THIS HEADER MAY NOT BE EXTRACTED OR MODIFIED IN ANY WAY.

package grpc

import fabric.FabricConnector
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.consumeAsFlow
import context.ContextOuterClass
import dlt.DltGateway
import dlt.DltGatewayServiceGrpcKt

class DLTService(private val connector: FabricConnector) :
    DltGatewayServiceGrpcKt.DltGatewayServiceCoroutineImplBase() {
    override suspend fun recordToDlt(request: DltGateway.DltRecord): DltGateway.DltRecordStatus {
        println("Incoming request ${request.recordId.recordUuid}")
        val error = when (request.operation) {
            DltGateway.DltRecordOperationEnum.DLTRECORDOPERATION_ADD -> {
                println("Adding new record")
                connector.putData(request)
            }
            DltGateway.DltRecordOperationEnum.DLTRECORDOPERATION_UPDATE -> {
                println("Updating record")
                connector.updateData(request)
            }
            DltGateway.DltRecordOperationEnum.DLTRECORDOPERATION_DELETE -> {
                println("Deleting record")
                connector.deleteData(request)
            }
            else -> "Undefined or unknown operation"
        }

        val dltStatusEnum: DltGateway.DltRecordStatusEnum = if (error == "") {
            DltGateway.DltRecordStatusEnum.DLTRECORDSTATUS_SUCCEEDED
        } else {
            DltGateway.DltRecordStatusEnum.DLTRECORDSTATUS_FAILED
        }
        return DltGateway.DltRecordStatus.newBuilder()
            .setRecordId(request.recordId)
            .setStatus(dltStatusEnum)
            .setErrorMessage(error)
            .build()
    }

    override suspend fun getFromDlt(request: DltGateway.DltRecordId): DltGateway.DltRecord {
        return connector.getData(request.recordUuid.uuid)
    }

    override fun subscribeToDlt(request: DltGateway.DltRecordSubscription): Flow<DltGateway.DltRecordEvent> {
        println("Subscription request: $request")
        return connector.subscribeForEvents().consumeAsFlow()
    }

    override suspend fun getDltStatus(request: ContextOuterClass.TeraFlowController): DltGateway.DltPeerStatus {
        return super.getDltStatus(request)
    }

    override suspend fun getDltPeers(request: ContextOuterClass.Empty): DltGateway.DltPeerStatusList {
        return super.getDltPeers(request)
    }
}