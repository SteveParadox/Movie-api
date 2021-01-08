import axios from "axios";
import { GET_ITEMS, SIGN_IN } from  "./types";

export const getItems = () => dispatch => {
    dispatch(setItemsLoading());
    axios
      .get("/")
      .then(res => {
        dispatch({
          type: GET_ITEMS,
          payload: res.data
        })
      })
};