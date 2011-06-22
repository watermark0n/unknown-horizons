# ###################################################
# Copyright (C) 2011 The Unknown Horizons Team
# team@unknown-horizons.org
# This file is part of Unknown Horizons.
#
# Unknown Horizons is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# ###################################################

from horizons.ai.aiplayer.building import AbstractBuilding
from horizons.ai.aiplayer.constants import BUILD_RESULT

from horizons.world.production.productionline import ProductionLine
from horizons.constants import BUILDINGS, RES
from horizons.util.python import decorators

class AbstractClayDeposit(AbstractBuilding):
	def __init__(self, building_id, name, production_line_ids):
		super(AbstractClayDeposit, self).__init__(building_id, name, [])
		self.lines = {} # output_resource_id: ProductionLine
		assert len(production_line_ids) == 1, 'expected exactly 1 production line'
		for production_line_id in production_line_ids:
			# create a fake production line that is similar to the clay pit one
			# TODO: use a better way of producing fake ProductionLine-s
			production_line = ProductionLine(production_line_id)
			production_line.id = None
			production_line.production = {}
			production_line.produced_res = {}
			for resource_id, amount in production_line.consumed_res.iteritems():
				production_line.production[resource_id] = -amount
				production_line.produced_res[resource_id] = -amount
			production_line.consumed_res = {}
			self.lines[RES.RAW_CLAY_ID] = production_line

	@classmethod
	def load(cls, db, building_id):
		# load the clay pit data because clay deposits don't actually produce anything
		production_line_ids = cls.load_production_line_ids(db, BUILDINGS.CLAY_PIT_CLASS)
		name = cls.load_name(db, building_id)
		return cls(building_id, name, production_line_ids)

	def build(self, settlement_manager, resource_id):
		return BUILD_RESULT.OK # TODO: check whether there are available clay deposits

	@classmethod
	def register_buildings(cls):
		cls.available_buildings[BUILDINGS.CLAY_DEPOSIT_CLASS] = cls

AbstractClayDeposit.register_buildings()

decorators.bind_all(AbstractClayDeposit)
