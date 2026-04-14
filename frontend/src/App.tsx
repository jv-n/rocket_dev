import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'
import Home from './Pages/Home'
import ListProducts from './Pages/List_Products'
import Product from './Pages/Product'
import Sales from './Pages/Sales'
import AppSidebar from './components/organisms/AppSidebar'

function App() {
  return (
    <Router>
      <Routes>
        <Route element={<AppSidebar />}>
          <Route path="/" element={<Home />} />
          <Route path="/products" element={<ListProducts />} />
          <Route path="/products/:id" element={<Product />} />
          <Route path='/sales' element={<Sales />} />
        </Route>
      </Routes>
    </Router>
  )
}

export default App
