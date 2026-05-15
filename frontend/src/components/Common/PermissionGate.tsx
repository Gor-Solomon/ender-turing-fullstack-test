import React from "react"
import useAuth from "@/hooks/useAuth"

interface PermissionGateProps {
  children: React.ReactNode
  allowedRoles: string[]
  showFallback?: boolean
}

const PermissionGate: React.FC<PermissionGateProps> = ({
  children,
  allowedRoles,
  showFallback = false,
}) => {
  const { user } = useAuth()

  // Ensure user is present and has one of the required roles
  const hasAccess = user && allowedRoles.includes(user.role)

  if (!hasAccess) {
    return showFallback ? (
      <div className="p-4 text-center text-red-500">
        You do not have permission to view this content.
      </div>
    ) : null
  }

  return <>{children}</>
}

export default PermissionGate
