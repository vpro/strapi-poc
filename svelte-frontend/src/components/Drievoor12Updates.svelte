<script lang="ts">
  import { request, gql } from 'graphql-request'
  import { useQuery, QueryClient  } from '@sveltestack/svelte-query'



  export let setPostId

  const client = new QueryClient({
    defaultOptions: {

      queries: {

      }
    }
  });
  const endpoint = 'http://localhost:1337/graphql'

  const posts = useQuery<
    { id: string; title: string; body: string }[],
    { message: string }
  >('Drievoor12Updates', async () => {
    const {
      posts: {data}
    } = await request(
      endpoint,
      gql`
        query {
          drievoor12Updates {
            data {
             attributes {
              title
              text
              uuid
              }
            }
          }
        }
      `
    )
    return data
  })
</script>

<div>
  <div>
    {#if $posts.status === 'loading'}
      Loading...
    {:else if $posts.status === 'error'}
      <span>Error: {$posts.error.message}</span>
    {:else}
      <div>
        {#each $posts.data as post}
          <p>
            <span
              on:click={() => setPostId(post.id)}
              style={
              // We can use the queryCache here to show bold links for
              // ones that are cached
              client.getQueryData([
                'Drievoor12Updates',
                post.id,
              ]) ? 'color: green; font-weight: bold; cursor: pointer;' : 'cursor: pointer;'}>
              {post.title}
            </span>
          </p>
        {/each}
      </div>
      <div>{$posts.isFetching ? 'Background Updating...' : ' '}</div>
    {/if}
  </div>
</div>
