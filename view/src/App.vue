<template>
	<h2>Показатели работы ППС университета за 2017 - 2019 гг.</h2>
	<StatisticTypes
		:types="types"
		v-model="types">
	</StatisticTypes>
	<a-collapse>
		<a-collapse-panel key="1" header="Общая статистика">
			<TotalStatistic
				:types="types"></TotalStatistic>
		</a-collapse-panel>
		<a-collapse-panel key="2" header="Статистика по факультетам">
			<FacultyStatistic
				:types="types"></FacultyStatistic>
		</a-collapse-panel>
		<a-collapse-panel key="3" header="Статистика по кафедрам">
			<ChairStatistic
				:types="types"></ChairStatistic>
		</a-collapse-panel>
	</a-collapse>
</template>

<script>

import TotalStatistic from "@/components/TotalStatistic";
import ChairStatistic from "@/components/ChairStatistic";
import FacultyStatistic from "@/components/FacultyStatistic";
import StatisticTypes from "@/components/StatisticTypes";
import {ref, watch} from 'vue'

export default {
	name: 'App',
	components: {
		TotalStatistic,
		ChairStatistic,
		FacultyStatistic,
		StatisticTypes,
	},
	setup() {
		const types = ref({
			'age': true,
			'experience': true,
			'position': true,
			'employment': true,
			'academic': true,
			'significant_publications': true,
			'other_publications': true,
			'extrabudgetary_funds': true
		});

		watch(() => types.value, (value) => {
			console.log(value.age)
		});


		return {
			types
		}
	}
}
</script>

<style>
#app {
	font-family: Avenir, Helvetica, Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
	text-align: center;
	color: #2c3e50;
	margin-top: 60px;
}
</style>
