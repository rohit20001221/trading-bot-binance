import Home from "../containers/Home";
import { IRoute } from "../containers/NavigationContainer";
import OrderDetail from "../containers/OrderDetail";

export const routes: IRoute = {
  home: {
    component: <Home />,
  },
  details: {
    component: <OrderDetail />,
  },
};
