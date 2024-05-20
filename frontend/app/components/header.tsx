import Image from "next/image";

export default function Header() {
  return (
    <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
      <p className="fixed left-0 top-0 flex w-full justify-center border-b border-gray-300 bg-gradient-to-b from-zinc-200 pb-6 pt-8 backdrop-blur-2xl dark:border-neutral-800 dark:bg-zinc-800/30 dark:from-inherit lg:static lg:w-auto  lg:rounded-xl lg:border lg:bg-gray-200 lg:p-4 lg:dark:bg-zinc-800/30">
        Ollama + llama-index querying&nbsp;
        <code className="font-mono font-bold">llama3-8b-text</code>
        &nbsp;with embedding using&nbsp;
        <code className="font-mono font-bold">snowflake-arctic-embed-m-long</code>
      </p>
      <div className="fixed bottom-0 left-0 flex h-48 w-full items-end justify-center bg-gradient-to-t from-white via-white dark:from-black dark:via-black lg:static lg:h-auto lg:w-auto lg:bg-none">
        <a
          href="https://scaleway.com/"
          className="flex items-center justify-center font-nunito text-lg font-bold gap-2"
        >
          <span>Running on Scaleway</span>
          <Image
            className="rounded-xl"
            src="/scaleway.png"
            alt="Scaleway logo"
            width={40}
            height={40}
            priority
          />
        </a>
      </div>
    </div>
  );
}