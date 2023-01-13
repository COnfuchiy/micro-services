<template>

	<StatisticTable
		v-if="statisticData"
		:statisticData="statisticData"
	/>
</template>

<script>
import StatisticTable from "@/components/StatisticTable";
import axios from "axios";
import {ref, watch} from "vue";
import {construct_query_params} from "@/types_constructor"

export default {
	components: {
		StatisticTable
	},
	name: "TotalStatistic",
	props: {
		types: {
			type: Object
		}
	},
	setup(props) {
		const statisticData = ref();
		const baseApiPath = process.env.VUE_APP_API_HOST + process.env.VUE_APP_API_PREFIX;

		watch(() => props.types, () => {
			axios.get(baseApiPath + process.env.VUE_APP_API_URL_STATISTIC + construct_query_params(props.types))
				.then(response => {
					statisticData.value = response.data
				})
				.catch(error => {
					console.log(error)
				});
		});

		axios.get(baseApiPath + process.env.VUE_APP_API_URL_STATISTIC + construct_query_params(props.types))
			.then(response => {
				statisticData.value = response.data
			})
			.catch(error => {
				console.log(error)
			});
		return {statisticData}
	},
	methods: {
		get() {
		}
	}
}
</script>

<style scoped>

</style>
