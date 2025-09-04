<script>
    import { onMount } from 'svelte';

    let projects_all = [];
    let loading = false;
    let sort_field = 'date';
    let sort_enable = true;
    let sort_asc = false;

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

    function set_sort(field) {
        sort_field = field;
        // off -> enable/asc -> enable/desc -> off
        if (!sort_enable) {
            sort_enable = true;
            sort_asc = true;
        } else { if (sort_asc) { sort_asc = false; } else { sort_enable = false; } }
    }

    function tbl_sort(field) {
        if ((sort_enable) && (sort_field === field)) {
            return sort_asc ? '▲' : '▼';
        }
        return '';
    }

    function get_sort(arr, field, enable, asc) {
        if (enable) {
            return [...arr].sort((a, b) => {
                if (typeof(a[field]) === 'number') {
                    if (asc) { return a[field] -             b[field];  } else { return b[field] -             a[field];  }
                } else {
                    if (asc) { return a[field].localeCompare(b[field]); } else { return b[field].localeCompare(a[field]); }
                }
            });
        } else {
            return arr;
        }
    }

    onMount(() => {
        api_all();
        setInterval(() => api_update(), 30*1000);
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
        <div class="p-2 border border-gray-400 col-span-1" on:click={() => set_sort('stay')}>Осталось {tbl_sort('stay')}</div>
        <div class="p-2 border border-gray-400 col-span-1" on:click={() => set_sort('reaction')}>Предл. {tbl_sort('reaction')}</div>
        <div class="p-2 border border-gray-400 col-span-2" on:click={() => set_sort('date')}>Дата {tbl_sort('date')}</div>
    </div>
    {#each get_sort(projects_all, sort_field, sort_enable, sort_asc) as project}
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
