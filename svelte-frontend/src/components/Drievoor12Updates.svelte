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
      `,
      {"Authorization": "Bearer 529aa5620e514391b3acccff6a095a277961c8f41a3ca128bd3c27fd870f80adfaefd13089bb60c614976147753291c11ec2cc58db249cf491e102ca5fc7e8cbc785cc0597ea80a257d9fbac8233bde7da44ea04c18e2da5d530e839f3dba4c7b4c9975416a0ae2078f4d4e822734a3ea54114d246d7842962bb10499df05df7"
      }
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
