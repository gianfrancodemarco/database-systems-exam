import { mutations } from "./mutations";
import { getters } from "./getters";
import { actions } from "./actions";
import { LotState } from "./state";

const defaultState: LotState = {
  lots: [],
  lot: null,
};

export const lotsModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};
