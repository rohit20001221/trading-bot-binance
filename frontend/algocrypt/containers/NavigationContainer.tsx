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
  navigate: (route: string) => void;
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

  const navigate: INavigationContext["navigate"] = (route) => {
    setCurrentRoute(route);
  };

  return (
    <NavigationContext.Provider value={{ routes, navigate }}>
      <StatusBar />
      {currentRoute && routes[currentRoute].header}
      {currentRoute && routes[currentRoute].component}
    </NavigationContext.Provider>
  );
};

export const useNavigation = () => useContext(NavigationContext);
