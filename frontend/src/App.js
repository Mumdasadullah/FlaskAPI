import RegistrationForm from "./component/RegistrationForm";
import LoginForm from "./component/LoginForm";
import { RouterProvider, createBrowserRouter } from 'react-router-dom'

function App() {
  const route = createBrowserRouter([
    {
      path: "/login",
      element: <LoginForm />
    },
    {
      path: "/register",
      element: <RegistrationForm />
    }
  ])
  return (
    <div>
      <RouterProvider router={route}></RouterProvider>
    </div>
  );
}

export default App;
