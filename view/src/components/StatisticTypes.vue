<template>
	<div>
		<label v-for="(key,type) in types" :key="type" :for="type">
			<input type="checkbox" :id="type" checked @change="onChange($event)"/>
			{{ this.viewNames[type] }}
		</label>
	</div>

</template>

<script>
import {defineEmits} from 'vue'

defineEmits(['update:modelValue'])
export default {
	name: "StatisticTypes",
	props: {
		types: {
			type: Object
		}
	},
	data() {
		return {
			viewNames: {
				'age': 'Средний возраст сотрудников',
				'experience': 'Среднее время работы в институте',
				'position': 'Должности',
				'employment': 'Ставки',
				'academic': 'Академические характеристики',
				'significant_publications': 'Знамчимые публикации',
				'other_publications': 'Публикации в Scopus/WoS',
				'extrabudgetary_funds': 'Поступление внебюджетных средств'
			}
		}
	},
	setup() {
	},
	methods: {
		onChange(event) {
			let newTypes = structuredClone(this.types)
			newTypes[event.target.id] = event.target.checked;

			this.$emit("update:modelValue", newTypes)
		}
	}
}
</script>

<style scoped>

</style>