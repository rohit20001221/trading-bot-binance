import { NavigationProvider } from "./containers/NavigationContainer";
import { routes } from "./navigation";

export default function App() {
  return <NavigationProvider routes={routes} />;
}
