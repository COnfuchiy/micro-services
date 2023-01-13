<template>
	<h4 class="text-start">Выберите факультет</h4>
	<select class="form-select" v-model="selectedFaculty">
		<option
			v-for="faculty in faculties"
			:key="faculty"
			:value="faculty"
		>
			{{ faculty }}
		</option>
	</select>
	<StatisticTable
		v-if="statisticData"
		:tableViewName="tableViewName"
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
	name: "FacultyStatistic",
	props: {
		types: {
			type: Object
		}
	},
	setup(props) {
		const statisticData = ref();
		const faculties = ref();
		const selectedFaculty = ref();
		const tableViewName = ref();
		const baseApiPath = process.env.VUE_APP_API_HOST + process.env.VUE_APP_API_PREFIX;


		watch(() => props.types, () => {
			if (selectedFaculty.value) {
				axios.get(baseApiPath + process.env.VUE_APP_API_URL_STATISTIC + "/" + selectedFaculty.value + "/" + construct_query_params(props.types))
					.then(response => {
						statisticData.value = response.data
						tableViewName.value = 'Статистика по факультету «' + selectedFaculty.value + '»'
					})
					.catch(error => {
						console.log(error)
					});
			}
		});

		watch(() => selectedFaculty.value, (value) => {
			axios.get(baseApiPath + process.env.VUE_APP_API_URL_STATISTIC + "/" + value + "/" + construct_query_params(props.types))
				.then(response => {
					statisticData.value = response.data
					tableViewName.value = 'Статистика по факультету «' + value + '»'
				})
				.catch(error => {
					console.log(error)
				});
		});


		axios.get(baseApiPath + process.env.VUE_APP_API_URL_FACULTIES_LIST)
			.then(response => {
				faculties.value = response.data.faculties
			})
			.catch(error => {
				console.log(error)
			});
		return {
			statisticData,
			faculties,
			selectedFaculty,
			tableViewName
		}
	}
}
</script>

<style scoped>

</style>