import { createContext, FC, useContext, ReactNode, useState } from "react";
import { StatusBar } from "react-native";

export type IRoute = {
  [route: string]: {
    component: ReactNode;
    header?: ReactNode;
  };
};

type INavigationContext = {
  routes: IRoute;
  navigate: (route: string, props?: Record<string, unknown>) => void;
  params?: Record<string, unknown>;
};

type NavigationProviderProps = {
  routes: IRoute;
};

export const NavigationContext = createContext<INavigationContext>({
  routes: {},
  navigate: () => {
    throw new Error("navigate not implemented");
  },
});

export const NavigationProvider: FC<NavigationProviderProps> = ({ routes }) => {
  const [currentRoute, setCurrentRoute] = useState(Object.keys(routes)[0]);
  const [navigationProps, setNavigationProps] =
    useState<Record<string, unknown>>();

  const navigate: INavigationContext["navigate"] = (route, props) => {
    setCurrentRoute(route);
    setNavigationProps(props);
  };

  return (
    <NavigationContext.Provider
      value={{ routes, navigate, params: navigationProps }}
    >
      <StatusBar />
      {currentRoute && routes[currentRoute].header}
      {currentRoute && routes[currentRoute].component}
    </NavigationContext.Provider>
  );
};

export const useNavigation = () => useContext(NavigationContext);
