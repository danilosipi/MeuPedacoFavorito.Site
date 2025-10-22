// Placeholder for tenant-related utility functions

/**
 * Gets the current tenant from the URL or other sources.
 * @returns The tenant identifier string.
 */
export function getCurrentTenant(): string {
  if (typeof window === 'undefined') {
    return 'default';
  }
  const pathSegments = window.location.pathname.split('/').filter(Boolean);
  if ((pathSegments[0] === 'client' || pathSegments[0] === 'public') && pathSegments.length > 1) {
    return pathSegments[1];
  }
  return 'default';
}
