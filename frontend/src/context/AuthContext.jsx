import { createContext, useContext, useState, useEffect } from "react";
import { api } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const refreshUser = async () => {
    try {
      const data = await api.auth.me();
      setUser(data);
      return data;
    } catch {
      setUser(null);
      return null;
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshUser();
  }, []);

  const login = async (email, password) => {
    const res = await api.auth.login({ email, password });
    if (res?.user) {
      setUser(res.user);
    } else {
      await refreshUser();
    }
    return res;
  };

  const register = async (data) => {
    return await api.auth.register(data);
  };

  const verifyOtp = async (email, otp) => {
    const res = await api.auth.verifyOtp({ email, otp });
    if (res?.user) {
      setUser(res.user);
    } else {
      await refreshUser();
    }
    return res;
  };

  const resendOtp = async (email) => {
    return await api.auth.resendOtp({ email });
  };

  const logout = async () => {
    try {
      await api.auth.logout();
    } finally {
      setUser(null);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        register,
        verifyOtp,
        resendOtp,
        logout,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return ctx;
}
