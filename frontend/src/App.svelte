<script lang="ts">
  import { onMount } from 'svelte';
  import Comments from './comments.svelte';

  let apiKey: string = '';
  let articles: any[] = [];
  let showComments = false;
  let currentArticleId = '';

  // template from slides
  const BASE_URL = 'https://api.nytimes.com/svc/search/v2/articlesearch.json';

  function makeRequest(query: string, apiKey: string) {
    const url = `${BASE_URL}?q=${encodeURIComponent(query)}&api-key=${apiKey}`;
    console.log("Requesting:", url);
    fetch(url)
      .then(statusCheck)
      .then((res) => res.json())
      .then(processData)
      .catch(handleError);
  }

  function processData(nytData: any) {
    console.log("NYT response: ", nytData);
    if (nytData.status === "OK" && nytData.response?.docs) {
      articles = nytData.response.docs;
      // creating article ID for comments
      articles = articles.map(article => {
        return {
          ...article,
          articleId: article._id.replace(/\//g, '-') 
        };
      });
    } else {
      console.error("Nyt response incorrect", nytData);
    }
  }

  async function statusCheck(res: Response) {
    if (!res.ok) {
      throw new Error(await res.text());
    }
    return res;
  }

  function handleError(err: any) {
    console.error("fetch error:", err.message);
  }

  onMount(async () => {
    try {
      const res = await fetch('/api/key');
      const data = await res.json();
      apiKey = data.apiKey;
      makeRequest("UC Davis", apiKey);
    } catch (error) {
      console.error('Failed to fetch API key:', error);
    }
  });

  function formatDate(dateString: string): string {
    // formats the date into month, year
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'long',
      year: 'numeric'
    });
  }

  function getImageURL(article: any): string {
    // returns the image URL if it exists
    if (!article || !article.multimedia || article.multimedia.length === 0) return '';

    // return default if not, then use thumbnail
    if (article.multimedia.default?.url) {
      return article.multimedia.default.url;
    } else if (article.multimedia.thumbnail?.url) {
      return article.multimedia.thumbnail.url;
    } else {
      // if no image dont show anything
      return '';
    }
  }

  // COMMENTING FUNCTIONS
  function openComments(articleId: string) {
    currentArticleId = articleId;
    showComments = true;
  }

  function handleCloseComments() {
    showComments = false;
  }
</script>

<main>
  <header>
    <!-- HEADER 1: title of the page-->
    <h1>The New York Times</h1>

    <!-- NAVIGATION BAR: used this source to help: https://www.w3schools.com/howto/howto_js_topnav.asp-->
    <div class="navbar">
      <a href="#">Current</a>
      <a href="#">Politics</a>
      <a href="#">Fitness</a>
      <a href="#">Cooking</a>
      <a href="#">Sports</a>
    </div>

    <!-- CURRENT DAY -->
    <div class="date-container">
      <p id="date"></p>
    </div>
  </header>

  <!-- JAVASCRIPT: used this source and previous knowledge of JS: https://www.w3schools.com/js/js_date_methods.asp-->
  <!-- prints out the current date and weekday-->
  <script>
    let date = new Date();
    let year = date.getFullYear();
    const months = ["January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"];
    let month = months[date.getMonth()];
    let day = date.getDate();
    const weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    let dayofweek = weekdays[date.getDay()];

    document.getElementById("date").innerHTML = dayofweek + " - " + month + " " + day + " " + year;  
  </script>

  <div class="columns-container">
    <div class="column">
      <!-- COLUMN 1 - top of hierarchy -->
      <article>
        <!-- clicking the image and headline directs to the full article-->
        <h2>
          <a class="headline" href={articles[0]?.web_url} target="_blank">
            {articles[0]?.headline.main}
          </a>
        </h2>

        <a href={articles[0]?.web_url} target="_blank">
          <img src={getImageURL(articles[0])} alt="Faculty on Strike"/>
        </a>

        <p>{articles[0]?.abstract}</p>
        <p>{articles[0]?.byline?.original}</p>
        <p>{formatDate(articles[0]?.pub_date)}</p>
        {#if articles[0]}
          <button class="comment-button" on:click={() => openComments(articles[0].articleId)}>💬 Comments</button>
        {/if}
      </article>

      <article>
        <a href={articles[1]?.web_url} target="_blank">
          <img src={getImageURL(articles[1])} alt="article 1"/>
        </a>

        <h2>
          <a class="headline" href={articles[1]?.web_url} target="_blank">
            {articles[1]?.headline.main}
          </a>
        </h2>

        <p>{articles[1]?.abstract}</p>
        <p>{articles[1]?.byline?.original}</p>
        <p>{formatDate(articles[1]?.pub_date)}</p>
        {#if articles[1]}
          <button class="comment-button" on:click={() => openComments(articles[1].articleId)}> 💬 Comments</button>
        {/if}
      </article>

      <article>
        <a href={articles[3]?.web_url} target="_blank">
          <img src={getImageURL(articles[3])} alt="article 3"/>
        </a>
        
        <h2>
          <a class="headline" href={articles[3]?.web_url} target="_blank">
            {articles[3]?.headline.main}
          </a>
        </h2>
  
        <p>{articles[3]?.abstract}</p>
        <p>{articles[3]?.byline?.original}</p>
        <p>{formatDate(articles[3]?.pub_date)}</p>
        {#if articles[3]}
          <button class="comment-button" on:click={() => openComments(articles[3].articleId)}>💬 Comments</button>
        {/if}
      </article>
    </div>
  
    <div class="column">
      <!-- COLUMN 2 NEXT-->
      <article>
        <a href={articles[2]?.web_url} target="_blank">
          <img src={getImageURL(articles[2])} alt="article 2"/>
        </a>

        <h2>
          <a class="headline" href={articles[2]?.web_url} target="_blank">
            {articles[2]?.headline.main}
          </a>
        </h2>

        <p>{articles[2]?.abstract}</p>
        <p>{articles[2]?.byline?.original}</p>
        <p>{formatDate(articles[2]?.pub_date)}</p>
        {#if articles[2]}
          <button class="comment-button" on:click={() => openComments(articles[2].articleId)}>💬 Comments</button>
        {/if}
      </article>

      <article>
        <a href={articles[4]?.web_url} target="_blank">
          <img src={getImageURL(articles[4])} alt="article 4 image"/>
        </a>

        <h2>
          <a class="headline" href={articles[4]?.web_url} target="_blank">
            {articles[4]?.headline.main}
          </a>
        </h2>

        <p>{articles[4]?.abstract}</p>
        <p>{articles[4]?.byline?.original}</p>
        <p>{formatDate(articles[4]?.pub_date)}</p>
        {#if articles[4]}
          <button class="comment-button" on:click={() => openComments(articles[4].articleId)}>💬 Comments</button>
        {/if}
      </article>

      <article>
        <a href={articles[5]?.web_url} target="_blank">
          <img src={getImageURL(articles[5])} alt="Faculty on Strike"/>
        </a>

        <h2>
          <a class="headline" href={articles[5]?.web_url} target="_blank">
            {articles[5]?.headline.main}
          </a>
        </h2>

        <p>{articles[5]?.abstract}</p>
        <p>{articles[5]?.byline?.original}</p>
        <p>{formatDate(articles[5]?.pub_date)}</p>
        {#if articles[5]}
          <button class="comment-button" on:click={() => openComments(articles[5].articleId)}>💬 Comments</button>
        {/if}
      </article>
    </div>

    <div class="column">
      <!-- COLUMN 3-->
      <article>
        <h2>
          <a class="headline" href={articles[6]?.web_url} target="_blank">
            {articles[6]?.headline.main}
          </a>
        </h2>

        <a href={articles[6]?.web_url} target="_blank">
          <img src={getImageURL(articles[6])} alt="Faculty on Strike"/>
        </a>

        <p>{articles[6]?.abstract}</p>
        <p>{articles[6]?.byline?.original}</p>
        <p>{formatDate(articles[6]?.pub_date)}</p>
        {#if articles[6]}
          <button class="comment-button" on:click={() => openComments(articles[6].articleId)}>💬 Comments</button>
        {/if}
      </article>

      <article>
        <a href={articles[7]?.web_url} target="_blank">
          <img src={getImageURL(articles[7])} alt="Faculty on Strike"/>
        </a>
        
        <h2>
          <a class="headline" href={articles[7]?.web_url} target="_blank">
            {articles[7]?.headline.main}
          </a>
        </h2>
      
        <p>{articles[7]?.abstract}</p>
        <p>{articles[7]?.byline?.original}</p>
        <p>{formatDate(articles[7]?.pub_date)}</p>
        {#if articles[7]}
          <button class="comment-button" on:click={() => openComments(articles[7].articleId)}>💬 Comments</button>
        {/if}
      </article>

      <article>
        <a href={articles[8]?.web_url} target="_blank">
          <img src={getImageURL(articles[8])} alt="Faculty on Strike"/>
        </a>

        <h2>
          <a class="headline" href={articles[8]?.web_url} target="_blank">
            {articles[8]?.headline.main}
          </a>
        </h2>
        
        <p>{articles[8]?.abstract}</p>
        <p>{articles[8]?.byline?.original}</p>
        <p>{formatDate(articles[8]?.pub_date)}</p>
        {#if articles[8]}
          <button class="comment-button" on:click={() => openComments(articles[8].articleId)}>💬 Comments</button>
        {/if}
      </article>
    </div>
  </div>

  <!-- use comments component -->
  <Comments
    articleId={currentArticleId}
    isOpen={showComments}
    on:close={handleCloseComments}
  />
</main>

<footer>
  <p>Homework #3 - ECS 162 - Web Programming</p>
</footer>