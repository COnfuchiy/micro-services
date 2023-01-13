<template>
	<h5 class="text-start" v-if="tableViewName">{{ tableViewName }}</h5>
	<table v-if="statisticData" class="table table-bordered table-striped">
		<thead>
		<tr>
			<th>Показатель</th>
			<th>Значение</th>
		</tr>
		</thead>
		<tbody>
		<tr class="text-start" v-for="item in data" :key="item.fieldName">
			<template v-if="Object.values(viewFields).includes(item.fieldName)">
				<td class="w-auto">{{ item.fieldName }}</td>
				<td class="w-auto" v-if="Array.isArray(item.value)">
                <span v-for="subItem in item.value" :key="subItem.name">
                    {{ subItem.name }} -
                    <span v-if="subItem.hasOwnProperty('count')">{{
							Number.isInteger(subItem.count) ? subItem.count : subItem.count.toFixed(2)
						}}</span>
                    <span v-else-if="subItem.hasOwnProperty('average')">{{
							Number.isInteger(subItem.average) ? subItem.average : subItem.average.toFixed(2)
						}}</span>
                    <span v-else>0</span>
                    <br>
                </span>
				</td>
				<td v-else>{{ item.value }}</td>
			</template>
		</tr>
		</tbody>
	</table>
</template>
<script>
export default {
	name: 'StatisticTable',
	props: {
		tableViewName: {
			type: String
		},
		statisticData: {
			type: Object,
		}
	},
	computed: {
		data() {
			console.log(this.statisticData)

			return Object.entries(this.statisticData).map(entry => {
				return {
					fieldName: this.viewFields[entry[0]],
					value: entry[1],
				}
			});
		}
	},
	setup() {
		const viewFields = {
				'employeeCount': 'Количество сотрудников',
				'ageAverage': 'Средний возраст сотрудников',
				'experienceAverage': 'Среднее время работы в институте',
				'positions': 'Должности',
				'employments': 'Ставки',
				'academicDegrees': 'Академические степени',
				'academicTitles': 'Академические звания',
				'significantPublications': 'Значимые публикации: всего',
				'significantPublicationsAverage': 'Значимые публикации: среднее',
				'otherPublications': 'Публикации в Scopus/WoS: всего',
				'otherPublicationsAverage': 'Публикации в Scopus/WoS: среднее',
				'extrabudgetaryFunds': 'Поступление внебюджетных средств: всего',
				'extrabudgetaryFundsAverage': 'Поступление внебюджетных средств: среднее',
			},
			headerFields = ['Показатель', 'Значение'];
		return {viewFields, headerFields}
	}
}
</script>
<style scoped>

</style>
