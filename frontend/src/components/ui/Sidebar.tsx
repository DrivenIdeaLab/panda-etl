"use client";
import React from "react";
import Link from "next/link";
import { X, Workflow, Folder, MessageCircle, Settings } from "lucide-react";
import { useSidebar } from "@/context/SidebarContext";
import { usePathname } from "next/navigation";
import LogoDark from "@/icons/LogoDark";

const routes = [
  {
    name: "Projects",
    path: "/projects",
    Icon: <Folder className="w-5 h-5 mr-2" />,
  },
  {
    name: "Processes",
    path: "/processes",
    Icon: <Workflow className="w-5 h-5 mr-2" />,
  },
];

const Sidebar: React.FC = () => {
  const { isSidebarOpen, setIsSidebarOpen } = useSidebar();
  const path = usePathname();

  return (
    <aside
      className={`w-64 bg-white shadow-md fixed h-full z-20 transition-transform duration-300 ease-in-out ${
        isSidebarOpen ? "translate-x-0" : "-translate-x-full"
      } md:translate-x-0`}
    >
      <div>
        <div className="flex justify-between items-center px-4">
          <Link href="/projects" className="flex justify-center items-center cursor-pointer w-[170px] pt-3">
            <LogoDark color="black"/>
            <h2 className="text-xl font-semibold">Panda{'{'}·{'}'}etl</h2>
          </Link>
          <button
            onClick={() => setIsSidebarOpen(false)}
            className="md:hidden focus:outline-none"
          >
            <X className="w-6 h-6 text-gray-500" />
          </button>
        </div>
        <div className="p-4">
          <ul className="mt-9">
            {routes.map((route) => (
              <li className="mb-2" key={route.path}>
                <Link
                  href={route.path}
                  className={`flex items-center hover:text-blue-500 ${
                    route.path === path
                      ? "text-black font-semibold"
                      : "text-gray-700"
                  }`}
                >
                  {route.Icon}
                  {route.name}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="absolute bottom-0 left-0 w-full p-4 border-t">
        <ul>
          <li className="mb-2">
            <a
              href="mailto:help@sinaptik.ai"
              className="flex items-center text-gray-700 hover:text-blue-500"
            >
              <MessageCircle className="w-5 h-5 mr-2" />
              Contact us
            </a>
          </li>
          <li className="mb-10">
            <Link
              href="/settings"
              className="flex items-center text-gray-700 hover:text-blue-500"
            >
              <Settings className="w-5 h-5 mr-2" />
              Settings
            </Link>
          </li>
          <li className="flex justify-between text-sm text-gray-500">
            <a
              href="https://sinaptik.notion.site/Terms-of-Service-6531411a9dfe4f1b9cb6045e93e9723c?pvs=4"
              className="hover:text-blue-500"
              target="_blank"
            >
              Terms
            </a>
            <a
              href="https://sinaptik.notion.site/Datenschutzrichtlinie-012906dd21f14443971247291fdbc474?pvs=4"
              className="hover:text-blue-500"
              target="_blank"
            >
              Privacy Policy
            </a>
          </li>
        </ul>
      </div>
    </aside>
  );
};

export default Sidebar;
