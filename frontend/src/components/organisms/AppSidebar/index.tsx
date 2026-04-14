import { Outlet, NavLink, useLocation } from "react-router-dom"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarInset,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/molecules/Sidebar/sidebar"
import { HugeiconsIcon } from "@hugeicons/react"
import { Rocket02Icon, Home03Icon, ShoppingBag01Icon, Chart01Icon } from "@hugeicons/core-free-icons"

const navItems = [
  { title: "Home", url: "/" },
  { title: "Produtos", url: "/products" },
  { title: "Vendas", url: "/sales" },
]

const setIcon = (title: string) => {
  switch (title) {
    case "Home":
      return <HugeiconsIcon icon={Home03Icon} className="w-4 h-4" color="#FFF" strokeWidth={2} />
    case "Produtos":
      return <HugeiconsIcon icon={ShoppingBag01Icon} className="w-4 h-4" color="#FFF" strokeWidth={2} />
    case "Vendas":
      return <HugeiconsIcon icon={Chart01Icon} className="w-4 h-4" color="#FFF" strokeWidth={2} />
    default:
      return null
  }
}

export default function AppSidebar() {
  const { pathname } = useLocation()
  console.log("Current path:", pathname)

  const isActive = (url: string) => {
    if (pathname === url){
    return "bg-primary" }
    else return "bg-primary/50"
  }

  return (
    <SidebarProvider defaultOpen>
      <Sidebar collapsible="icon">
        <SidebarHeader className="group-data-[collapsible=icon]:p-3 bg-secondary border-b mb-2" >
          <HugeiconsIcon icon={Rocket02Icon} className="w-6 h-6" color="#1447e6" strokeWidth={1.8} />
          <span className="group-data-[collapsible=icon]:hidden px-3 py-2 text-sm font-bold">Rocket E-Commerce</span>
        </SidebarHeader>
        <SidebarContent>
          <SidebarGroup className="group-data-[collapsible=icon]:hidden">
            <SidebarGroupLabel className="px-2 text-xs font-semibold uppercase text-muted-foreground">
              Navegação
            </SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu className="w-full rounded-lg bg-secondary p-2 gap-2 shadow-sm">
                {navItems.map((item) => (
                  <SidebarMenuItem key={item.title}>
                    <SidebarMenuButton
                      className={`gap-2 text-primary-foreground hover:bg-primary/80 hover:text-primary-foreground ${isActive(item.url)}`}
                      asChild
                    >
                      <NavLink to={item.url} end>
                        {setIcon(item.title)}
                        <span>{item.title}</span>
                      </NavLink>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                ))}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>

  {/* Collapsed: show icons only */}
          <SidebarGroup className="hidden group-data-[collapsible=icon]:block">
            <SidebarGroupContent>
              <SidebarMenu className="gap-2">
                {navItems.map((item) => (
                  <SidebarMenuItem key={item.title}>
                    <SidebarMenuButton
                      className={`text-primary-foreground hover:bg-primary/80 hover:text-primary-foreground justify-center ${isActive(item.url)}`}
                      asChild
                      tooltip={item.title}
                    >
                      <NavLink to={item.url} end>
                        {setIcon(item.title)}
                      </NavLink>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                ))}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        </SidebarContent>
        <SidebarFooter className="group-data-[collapsible=icon]:hidden rounded-t-lg border-t bg-secondary p-4 text-center">
          <span className="text-xs text-muted-foreground">
            E-Commerce Manager © 2026
          </span>
        </SidebarFooter>
      </Sidebar>
      <SidebarInset>
        <header className="flex h-12 items-center gap-2 px-4 border-b">
          <SidebarTrigger />
        </header>
        <div className="flex flex-1 flex-col gap-4 p-4">
          <Outlet />
        </div>
      </SidebarInset>
    </SidebarProvider>
  )
}
