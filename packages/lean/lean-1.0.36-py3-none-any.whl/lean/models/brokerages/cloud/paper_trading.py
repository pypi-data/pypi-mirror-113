# QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
# Lean CLI v1.0. Copyright 2021 QuantConnect Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Dict

from lean.components.util.logger import Logger
from lean.models.brokerages.cloud.base import CloudBrokerage


class PaperTradingBrokerage(CloudBrokerage):
    """A CloudBrokerage implementation for paper trading."""

    @classmethod
    def get_id(cls) -> str:
        return "QuantConnectBrokerage"

    @classmethod
    def get_name(cls) -> str:
        return "Paper Trading"

    @classmethod
    def build(cls, logger: Logger) -> CloudBrokerage:
        return PaperTradingBrokerage()

    def _get_settings(self) -> Dict[str, str]:
        return {
            "environment": "paper"
        }
