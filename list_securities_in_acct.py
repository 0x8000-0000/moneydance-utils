#!/usr/bin/env python
# Python script to be run in Moneydance to perform amazing feats of financial scripting

from com.infinitekind.moneydance.model import *

import sys
import time

# get the default environment variables, set by Moneydance
print("The Moneydance app controller: %s" % (moneydance))
print("The current data set: %s" % (moneydance_data))
print("The UI: %s" % (moneydance_ui))
print("Bot interface: %s" % (moneybot))

if moneydance_data:
    txnSet = moneydance_data.getTransactionSet()

    usefulTxn = []

    for txn in txnSet.iterableTxns():
        account = txn.getAccount()
        if (
            account.getAccountName()
            == "Vanguard Short-Term Bond Index Fund Admiral Shares"
        ):
            usefulTxn.append(txn)

    sortedTxn = sorted(usefulTxn, key=lambda x: x.getDateInt())

    runningSum = 0
    runningSumByYear = 0
    currentYear = 0

    for txn in sortedTxn:
        year = txn.getDateInt() / 10000
        month = (txn.getDateInt() - year * 10000) / 100
        day = txn.getDateInt() - year * 10000 - month * 100
        if year != currentYear:
            if year != 0:
                print(
                    "for year %u: total shares: %12.4f"
                    % (currentYear, runningSum / 10000.0)
                )
                print("")
            currentYear = year
        if txn.getValue() != 0:
            runningSum += txn.getValue()
            print(
                "    %4u-%02u-%02u %12.3f  @   $ %10.2f       running: %12.3f"
                % (
                    year,
                    month,
                    day,
                    txn.getValue() / 10000.0,
                    txn.getAmount() / 100.0,
                    runningSum / 10000.0,
                )
            )

    print("")
    print("partial year %u: total shares: %12.4f" % (currentYear, runningSum / 10000.0))
    print("")
