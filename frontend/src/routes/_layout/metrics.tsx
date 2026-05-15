import { createFileRoute, redirect } from "@tanstack/react-router"
import { UsersService } from "@/client"

export const Route = createFileRoute("/_layout/metrics")({
  component: Metrics,
  beforeLoad: async () => {
    const user = await UsersService.readUserMe()
    if (!user.is_superuser && user.role !== "admin" && user.role !== "manager") {
      throw redirect({
        to: "/",
      })
    }
  },
})

function Metrics() {
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Metrics</h1>
        <p className="text-muted-foreground">
          View application performance and usage insights
        </p>
      </div>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <div className="rounded-xl border bg-card text-card-foreground shadow">
          <div className="p-6">
            <h3 className="font-semibold leading-none tracking-tight">Status</h3>
            <p className="text-sm text-muted-foreground mt-2">Operational</p>
          </div>
        </div>
        <div className="rounded-xl border bg-card text-card-foreground shadow">
          <div className="p-6">
            <h3 className="font-semibold leading-none tracking-tight">Active Users</h3>
            <p className="text-sm text-muted-foreground mt-2">124</p>
          </div>
        </div>
        <div className="rounded-xl border bg-card text-card-foreground shadow">
          <div className="p-6">
            <h3 className="font-semibold leading-none tracking-tight">System Load</h3>
            <p className="text-sm text-muted-foreground mt-2">Low</p>
          </div>
        </div>
      </div>
      <div className="p-4 bg-muted rounded-lg">
        <p className="text-sm italic">Note: These are dummy metrics for the RBAC demonstration.</p>
      </div>
    </div>
  )
}
