# Copyright (C) 2018-2024 The python-bitcoin-utils developers
# Copyright (C) 2024 The python-blackcoin-utils developers
#
# This file is part of python-blackcoin-utils
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-blackcoin-utils, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.


from blackcoinutils.setup import setup
from blackcoinutils.utils import to_satoshis
from blackcoinutils.transactions import Transaction, TxInput, TxOutput, Sequence
from blackcoinutils.keys import P2pkhAddress, PrivateKey
from blackcoinutils.script import Script
from blackcoinutils.constants import TYPE_RELATIVE_TIMELOCK


def main():
    # always remember to setup the network
    setup("mainnet")

    #
    # This script spends from a P2SH address containing a CSV+P2PKH script as
    # created from examples/create_p2sh_csv_p2pkh.py
    #
    # We assume that some 11.1 tBTC have been send to that address and that we know
    # the txid and the specific UTXO index (or vout).
    #

    # set values
    relative_blocks = 20
    txid = "9d84b05ecc9bbdffa4590ff7b64602fa2955536331b2d3294fd1501944b35ebd"
    vout = 0

    seq = Sequence(TYPE_RELATIVE_TIMELOCK, relative_blocks)
    seq_for_n_seq = seq.for_input_sequence()
    assert seq_for_n_seq is not None

    # create transaction input from tx id of UTXO (contained 11.1 tBTC)
    txin = TxInput(txid, vout, sequence=seq_for_n_seq)

    # secret key needed to spend P2PKH that is wrapped by P2SH
    p2pkh_sk = PrivateKey("PgxxTGsyU2L7iD9HemZk8bjVCSjYyDNqiM2TJdAjr5VuLnZLjYJB")
    p2pkh_pk = p2pkh_sk.get_public_key().to_hex()
    p2pkh_addr = p2pkh_sk.get_public_key().get_address()

    # create the redeem script - needed to sign the transaction
    redeem_script = Script(
        [
            seq.for_script(),
            "OP_CHECKSEQUENCEVERIFY",
            "OP_DROP",
            "OP_DUP",
            "OP_HASH160",
            p2pkh_addr.to_hash160(),
            "OP_EQUALVERIFY",
            "OP_CHECKSIG",
        ]
    )

    # to confirm that address is the same as the one that the funds were sent
    # addr = P2shAddress.from_script(redeem_script)
    # print(addr.to_string())

    # send/spend to any random address
    to_addr = P2pkhAddress("B6si6dknPTc1qF9av3AU9awyUAJ3cfiQRu")
    txout = TxOutput(to_satoshis(0.999), to_addr.to_script_pub_key())

    # no change address - the remaining 0.1 tBTC will go to miners)

    # create transaction from inputs/outputs
    tx = Transaction([txin], [txout])

    # print raw transaction
    print("\nRaw unsigned transaction:\n" + tx.serialize())

    # use the private key corresponding to the address that contains the
    # UTXO we are trying to spend to create the signature for the txin -
    # note that the redeem script is passed to replace the scriptSig
    sig = p2pkh_sk.sign_input(tx, 0, redeem_script)
    # print(sig)

    # set the scriptSig (unlocking script) -- unlock the P2PKH (sig, pk) plus
    # the redeem script, since it is a P2SH
    txin.script_sig = Script([sig, p2pkh_pk, redeem_script.to_hex()])
    signed_tx = tx.serialize()

    # print raw signed transaction ready to be broadcasted
    print("\nRaw signed transaction:\n" + signed_tx)
    print("\nTxId:", tx.get_txid())


if __name__ == "__main__":
    main()
