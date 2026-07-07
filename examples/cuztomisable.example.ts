/**
 * Example: Fetching public Cuztomisable settings for use in your frontend.
 *
 * GET /api/cuztomisable/settings returns the subset of backend settings safe to
 * expose to clients (login/registration requirements, password rules, country
 * codes) — never secrets like jwt_secret.
 *
 * Copy this into your frontend project (e.g. src/services/cuztomisable.ts) and
 * adjust BASE_URL / the fetch call to match your app's existing API client.
 */

const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api'

export interface LoginSettings {
  with_email: boolean
  with_phone: boolean
  remember: boolean
}

export interface RegistrationSettings {
  require_username: boolean
  require_phone: boolean
}

export interface PasswordRequirements {
  min_length: number
  max_length: number | null
  uppercase: number | null
  digits: number | null
  special: number | null
}

export interface CountryCode {
  value: number
  label: string
  required_length: number
}

export interface CuztomisableSettings {
  login: LoginSettings
  registration: RegistrationSettings
  password_requirements: PasswordRequirements
  country_codes: CountryCode[]
  default_country_code: number
  default_language: string
}

export const cuztomisableService = {
  getSettings: async (): Promise<CuztomisableSettings> => {
    const res = await fetch(`${BASE_URL}/cuztomisable/settings`)
    if (!res.ok) {
      throw new Error(`Failed to load Cuztomisable settings: ${res.status}`)
    }
    return res.json()
  },
}
