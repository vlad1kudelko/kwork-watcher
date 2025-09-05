<script>
    import { onMount } from 'svelte';

    let loading     = $state(false);
    let sort_field  = $state('date');
    let sort_enable = $state(true);
    let sort_asc    = $state(false);
    let search      = $state('');

    let projects_all_raw = $state([]);
    let projects_all_calc = $derived.by(() => {
        // >>> search <<<<
        let local_arr = [...projects_all_raw].filter((item) => {
            return item.h1  .toLowerCase().includes(search.toLowerCase()) ||
                   item.text.toLowerCase().includes(search.toLowerCase());
        });
        // >>> sort_enable <<<
        if (!sort_enable) { return local_arr; }
        // >>> sort_field <<<
        if (local_arr.length === 0) { return local_arr; }
        let type_field = typeof(local_arr[0][sort_field]);  // находим тип поля, по которому производится сортировка
        let func_sort = undefined;                          // определяем функцию сортировки
        if (type_field === 'number') { func_sort = (a, b) => a[sort_field] - b[sort_field] }               // если поле числовое
        if (type_field === 'string') { func_sort = (a, b) => a[sort_field].localeCompare(b[sort_field]) }  // если поле строковое
        let local_arr_sort = [...local_arr].sort(func_sort);
        // >>> sort_asc <<<
        if (!sort_asc) { return local_arr_sort.reverse(); }
        return local_arr_sort;
    });
    $effect(() => {
        projects_all_calc;
        function add_selection(el, start, len) {
            let range = new Range();
            range.setStart(el.firstChild, start);
            range.setEnd(el.firstChild, start + len);
            window.getSelection().addRange(range);
        }
        window.getSelection().removeAllRanges();
        for (let selector of ['.my-field-h1', '.my-field-text']) {
            [...document.querySelectorAll(selector)].slice(0, 10).forEach((el) => {
                if (el.innerText.toLowerCase().includes(search.toLowerCase())) {
                    add_selection(el, el.innerText.toLowerCase().indexOf(search.toLowerCase()), search.length);
                }
            });
        }
    });

    async function api_update() {
        loading = true;
        const res = await fetch('/api/update');
        const json = await res.json();
        projects_all_raw = json;
        loading = false;
    }

    async function api_all() {
        loading = true;
        const res = await fetch('/api/all');
        const json = await res.json();
        projects_all_raw = json;
        loading = false;
    }

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

    onMount(() => {
        api_all();
        setInterval(() => api_update(), 30*1000);
    });
</script>

<div class="container mx-auto p-10 pb-0">
    <div class="flex items-center justify-between">
        <div class="font-bold text-2xl">{projects_all_raw.length} / {projects_all_calc.length}</div>
        <div class="bg-gray-200 text-gray-800 rounded-md px-4 py-2 cursor-pointer" onclick={api_update}>{loading ? 'Обновление...' : 'Обновить'}</div>
    </div>
    <input type="text" class="p-4 mt-4 block w-full bg-gray-800 outline-none" placeholder="Поиск" bind:value={search}>
</div>

<div class="p-10">
    <div class="grid grid-cols-19">
        <div class="p-2 border border-gray-400 col-span-1" >Ссылка</div>
        <div class="p-2 border border-gray-400 col-span-2" >Название</div>
        <div class="p-2 border border-gray-400 col-span-1" >Цена осн.</div>
        <div class="p-2 border border-gray-400 col-span-1" >Цена доп.</div>
        <div class="p-2 border border-gray-400 col-span-10">Описание</div>
        <div class="p-2 border border-gray-400 col-span-1" onclick={() => set_sort('stay')}>Осталось {tbl_sort('stay')}</div>
        <div class="p-2 border border-gray-400 col-span-1" onclick={() => set_sort('reaction')}>Предл. {tbl_sort('reaction')}</div>
        <div class="p-2 border border-gray-400 col-span-2" onclick={() => set_sort('date')}>Дата {tbl_sort('date')}</div>
    </div>
    {#each projects_all_calc as project}
        <div class="grid grid-cols-19">
            <div class="p-2 border border-gray-400 col-span-1  my-field-link      "><a href={project.link}>link</a></div>
            <div class="p-2 border border-gray-400 col-span-2  my-field-h1        ">{project.h1}</div>
            <div class="p-2 border border-gray-400 col-span-1  my-field-price-main">{project.price_main}</div>
            <div class="p-2 border border-gray-400 col-span-1  my-field-price-sub ">{project.price_sub}</div>
            <div class="p-2 border border-gray-400 col-span-10 my-field-text      ">{project.text}</div>
            <div class="p-2 border border-gray-400 col-span-1  my-field-stay      ">{project.stay}</div>
            <div class="p-2 border border-gray-400 col-span-1  my-field-reaction  ">{project.reaction}</div>
            <div class="p-2 border border-gray-400 col-span-2  my-field-date      ">{project.date}</div>
        </div>
    {/each}
</div>
