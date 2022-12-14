<template>
  <v-container fluid>
    <validation-observer ref="observer" v-slot="{ invalid }">
      <form @submit.prevent="onSubmit" @reset.prevent="onReset">
        <v-card class="ma-3 pa-3">
          <v-card-title primary-title>
            <div class="headline primary--text">Create Recipe</div>
          </v-card-title>
          <v-card-text>
            <div class="my-3">
              <div class="subheading secondary--text text--lighten-2">Id</div>
              <div v-if="recipe" class="title primary--text text--darken-2">
                {{ recipe.id }}
              </div>
              <div v-else class="title primary--text text--darken-2">-----</div>
            </div>
            <validation-provider v-slot="{ errors }" name="Name" rules="required">
              <v-text-field
                v-model="recipe.name"
                label="Name"
                required
                :error-messages="errors"
              ></v-text-field>
            </validation-provider>
            <validation-provider
              v-slot="{ errors }"
              rules="required"
              name="Description"
            >
              <v-text-field
                v-model="recipe.description"
                label="Description"
                required
                :error-messages="errors"
              ></v-text-field>
            </validation-provider>
            <validation-provider v-slot="{ errors }" name="Fruits">
              <v-select
                class="mt-7"
                v-model="recipe.fruits"
                :items="fruits"
                multiple
                label="Fruits used by this recipe"
                :error-messages="errors"
                :item-text="(item) => `${item.id} - ${item.name}`"
                item-value="id"
                dense
              />
            </validation-provider>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn @click="cancel">Cancel</v-btn>
            <v-btn :disabled="invalid" type="submit" color="primary"> Save </v-btn>
          </v-card-actions>
        </v-card>
      </form>
    </validation-observer>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { IRecipeUpdate } from "@/interfaces";
import { dispatchUpdateRecipe, dispatchGetRecipe } from "@/store/recipes/actions";
import { dispatchGetFruits } from "@/store/fruits/actions";
import { readFruits } from "@/store/fruits/getters";
import { readRecipe } from "@/store/recipes/getters";
import { ValidationProvider, ValidationObserver, extend } from "vee-validate";
import { required, confirmed, email } from "vee-validate/dist/rules";

extend("required", { ...required, message: "{_field_} can not be empty" });
extend("confirmed", { ...confirmed, message: "Passwords do not match" });
extend("email", { ...email, message: "Invalid email address" });

@Component({
  components: {
    ValidationObserver,
    ValidationProvider,
  },
})
export default class EditRecipe extends Vue {
  $refs!: {
    observer: InstanceType<typeof ValidationObserver>;
  };

  public async mounted() {
    await dispatchGetRecipe(this.$store, { id: this.$route.params.id });
    await dispatchGetFruits(this.$store);
  }

  public cancel() {
    this.$router.back();
  }

  public async onSubmit() {
    const success = await this.$refs.observer.validate();
    if (!success) {
      return;
    }

    const updatedRecipe: IRecipeUpdate = {
      id: this.recipe.id,
      name: this.recipe.name,
      description: this.recipe.description,
      fruits: this.recipe.fruits,
    };

    await dispatchUpdateRecipe(this.$store, {
      id: this.recipe.id,
      recipe: updatedRecipe,
    });

    this.$router.push("/main/recipes");
  }
  get recipe() {
    return readRecipe(this.$store);
  }
  get fruits() {
    return readFruits(this.$store);
  }
}
</script>
