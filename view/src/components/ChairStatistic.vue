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
	<div class="mt-3">
		<h4 class="text-start">Выберите кафедру</h4>
		<select class="form-select" v-if="selectedFaculty" v-model="selectedChair">
			<option
				v-for="chair in chairs"
				:key="chair"
				:value="chair"
			>
				{{ chair }}
			</option>
		</select>
	</div>

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
	name: "ChairStatistic",
	props: {
		types: {
			type: Object
		}
	},
	setup(props) {
		const statisticData = ref()
		const faculties = ref()
		const chairs = ref()
		const selectedFaculty = ref();
		const selectedChair = ref();
		const tableViewName = ref();
		const baseApiPath = process.env.VUE_APP_API_HOST + process.env.VUE_APP_API_PREFIX;

		watch(() => props.types, () => {
			if (selectedFaculty.value && selectedChair.value) {
				axios.get(baseApiPath + process.env.VUE_APP_API_URL_STATISTIC + "/" + selectedFaculty.value + "/" + selectedChair.value + "/" + construct_query_params(props.types))
					.then(response => {
						statisticData.value = response.data
						tableViewName.value = 'Статистика по кафедре «' + selectedChair.value + '»'
					})
					.catch(error => {
						console.log(error)
					});
			}

		});

		watch(() => selectedFaculty.value, (value) => {
			axios.get(baseApiPath + process.env.VUE_APP_API_URL_CHAIRS_LIST + "/" + value + "/")
				.then(response => {
					chairs.value = response.data.chairs
				})
				.catch(error => {
					console.log(error)
				});
		});


		watch(() => selectedChair.value, (value) => {
			axios.get(baseApiPath + process.env.VUE_APP_API_URL_STATISTIC + "/" + selectedFaculty.value + "/" + value + "/" + construct_query_params(props.types))
				.then(response => {
					statisticData.value = response.data
					tableViewName.value = 'Статистика по кафедре «' + value + '»'
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
			chairs,
			selectedFaculty,
			selectedChair,
			tableViewName
		}
	}
}
</script>

<style scoped>

</style>