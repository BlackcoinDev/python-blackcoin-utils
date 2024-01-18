# Copyright (C) 2018-2022 The python-bitcoin-utils developers
#
# This file is part of python-bitcoin-utils
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-bitcoin-utils, including this file, may be copied,
# modified, propagated, or distributed except according to the terms contained
# in the LICENSE file.

from bitcoinutils.setup import setup
from bitcoinutils.keys import P2trAddress, PrivateKey


def main():
    # always remember to setup the network
    setup("mainnet")

    # could also instantiate from existing WIF key
    priv = PrivateKey.from_wif("PdiUUh8dnXB36B2XcbPdodUX5Ujoj2VDubJwcW1V8DJu69XHZWGg")

    # compressed is the default
    print("\nPrivate key WIF:", priv.to_wif())

    # get the public key
    pub = priv.get_public_key()

    # public keys
    print("Public key as usual:", pub.to_hex())
    print("Taproot tweaked public key:", pub.to_taproot_hex())

    # get address from public key
    address = pub.get_taproot_address()

    # print the address and hash - default is compressed address
    print("Native Address:", address.to_string())
    taproot_pk = address.to_witness_program()
    print("Taproot witness program:", taproot_pk)
    print("Segwit Version:", address.get_type())

    # test to_string
    addr2 = P2trAddress.from_witness_program(taproot_pk)
    print("Created P2trAddress from public key and calculate address:")
    print("Native Address:", addr2.to_string())

    assert (
        address.to_string()
        == "blk1pmfr3p9j00pfxjh0zmgp99y8zftmd3s5pmedqhyptwy6lm87hf5ssm5w44w"
    )
    assert (
        addr2.to_string()
        == "blk1pmfr3p9j00pfxjh0zmgp99y8zftmd3s5pmedqhyptwy6lm87hf5ssm5w44w"
    )


if __name__ == "__main__":
    main()
