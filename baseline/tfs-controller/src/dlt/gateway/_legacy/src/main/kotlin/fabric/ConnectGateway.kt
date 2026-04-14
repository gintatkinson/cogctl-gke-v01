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

package fabric

import org.hyperledger.fabric.gateway.Contract
import org.hyperledger.fabric.gateway.Gateway
import org.hyperledger.fabric.gateway.Wallet
import java.nio.file.Paths

// helper function for getting connected to the gateway
fun getContract(config: proto.Config.DltConfig, wallet: Wallet): Contract {
    // load a CCP
    val networkConfigPath = Paths.get(config.connectionFile)
    val builder = Gateway.createBuilder()
    builder.identity(wallet, config.user).networkConfig(networkConfigPath).discovery(true)
    val gateway = builder.connect()
    val network = gateway.getNetwork(config.channel)
    return network.getContract(config.contract)
}