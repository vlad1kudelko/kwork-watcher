<script>
    import { onMount } from 'svelte';

    let projects_all = [];
    let loading = false;

    async function api_update() {
        loading = true;
        const res = await fetch('/api/update');
        const json = await res.json();
        projects_all = json;
        loading = false;
    }

    async function api_all() {
        loading = true;
        const res = await fetch('/api/all');
        const json = await res.json();
        projects_all = json;
        loading = false;
    }

    function rm_txt (txt) {
        if (txt === null) { return ''; }
        if (txt.includes(': ')) {
            return txt.split(': ')[1];
        } else { return txt; }
    };

    onMount(() => {
        api_all();
    });
</script>

<div class="container mx-auto p-10 pb-0">
    <div class="flex items-center justify-between">
        <div>Admin ({projects_all.length})</div>
        <div class="bg-gray-200 text-gray-800 rounded-md px-4 py-2 cursor-pointer" on:click={api_update}>{loading ? 'Обновление...' : 'Обновить'}</div>
    </div>
</div>

<div class="p-10">
    <div class="grid grid-cols-19">
        <div class="p-2 border border-gray-400 col-span-1" >Ссылка</div>
        <div class="p-2 border border-gray-400 col-span-2" >Название</div>
        <div class="p-2 border border-gray-400 col-span-1" >Цена осн.</div>
        <div class="p-2 border border-gray-400 col-span-1" >Цена доп.</div>
        <div class="p-2 border border-gray-400 col-span-10">Описание</div>
        <div class="p-2 border border-gray-400 col-span-1" on:click={projects_all = projects_all.sort((a, b) => b.stay - a.stay)}>Осталось</div>
        <div class="p-2 border border-gray-400 col-span-1" on:click={projects_all = projects_all.sort((a, b) => b.reaction - a.reaction)}>Предложений</div>
        <div class="p-2 border border-gray-400 col-span-2" on:click={projects_all = projects_all.sort((a, b) => b.date - a.date)}>Дата</div>
    </div>
    {#each projects_all as project}
        <div class="grid grid-cols-19">
            <div class="p-2 border border-gray-400 col-span-1" ><a href={project.link}>link</a></div>
            <div class="p-2 border border-gray-400 col-span-2" >{project.h1}</div>
            <div class="p-2 border border-gray-400 col-span-1" >{rm_txt(project.price_main)}</div>
            <div class="p-2 border border-gray-400 col-span-1" >{rm_txt(project.price_sub)}</div>
            <div class="p-2 border border-gray-400 col-span-10">{project.text}</div>
            <div class="p-2 border border-gray-400 col-span-1" >{project.stay}</div>
            <div class="p-2 border border-gray-400 col-span-1" >{project.reaction}</div>
            <div class="p-2 border border-gray-400 col-span-2" >{project.date}</div>
        </div>
    {/each}
</div>
