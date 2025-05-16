<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  export let articleId: string;
  export let isOpen = false;

  const dispatch = createEventDispatcher();

  let comments = [];
  let newComment = { user: '', text: '' };
  let replyTo: string | null = null;

  // fetch comments associated with the article and  when the comment button is opened 
  $: if (isOpen && articleId) fetchComments();
  $: if (isOpen) {
  replyTo = null;
}


  async function fetchComments() {
    try {
      const res = await fetch(`/api/comments/${articleId}`);
      comments = res.ok ? await res.json() : [];
    } catch {
      comments = [];
    }
  }

  // POST COMMENTS
  async function submitComment() {
    if (!newComment.user.trim() || !newComment.text.trim()) {
      alert('Please enter your name and comment');
      return;
    }

    const data = {
      article_id: articleId,
      user: newComment.user,
      text: newComment.text,
      parent_id: replyTo
    };

    try {
      const res = await fetch('/api/comments', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
      });
      if (res.ok) {
        newComment = { user: '', text: '' };
        replyTo = null;
        fetchComments();
      } else {
        alert('Failed to post comment');
      }
    } catch {
      alert('Error posting comment');
    }
  }

  function startReply(id: string) {
    replyTo = id;
    setTimeout(() => {
      document.getElementById('comment-form')?.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  }

  // CREATES HIERARCHY FOR REPLIES 
    function organizeComments(flatComments) {
    const map = new Map();
    flatComments.forEach(c => map.set(c.id, {...c, replies: []}));
    const roots = [];

    flatComments.forEach(c => {
        if (c.parent_id && map.has(c.parent_id)) {
        const parent = map.get(c.parent_id);
        if (!parent.parent_id) {
            parent.replies.push(map.get(c.id));
        } else {
            roots.push(map.get(c.id));
        }
        } else {
        roots.push(map.get(c.id));
        }
    });

    return roots;
    }


  function closeComments() {
  dispatch('close');
}

</script>


<!-- SIDE PANEL FOR COMMENTS -->
{#if isOpen}
  <div class="comments-panel">
    <div class="comments-header">
      <h2>Comments</h2>
      <button class="close-button" on:click={closeComments}>×</button>
    </div>
    
    <div class="comments-content">
      <div class="comment-form" id="comment-form">
        <h3>{replyTo ? 'Reply to comment' : 'Add a comment'}</h3>
        {#if replyTo}
          <div class="reply-info">
            <span>Replying to a comment</span>
          </div>
        {/if}
        <input 
          type="text" 
          placeholder="Name" 
          bind:value={newComment.user}
        />
        <textarea 
          placeholder="enter your comment here" 
          bind:value={newComment.text}
        ></textarea>
        <button class="submit-button" on:click={submitComment}>
          {replyTo ? 'Post Reply' : 'Post Comment'}
        </button>
      </div>

      <!-- COMMENTS -->
      <div class="comments-list">
        {#if comments.length === 0}
        <!-- if no comments yet, encourage to be the first-->
          <p class="no-comments">Be the first to comment!</p>
        {:else}

            <!-- ORGANIZE THE COMMENTS -->
          {#each organizeComments(comments) as comment}
            <div class="comment">
              <div class="comment-header">
                <strong>{comment.user}</strong>
              </div>
              <div class="comment-body">
                <p>{comment.text}</p>
              </div>
              <div class="comment-footer">
                <button class="reply-button" on:click={() => startReply(comment.id)}>Reply</button>
              </div>
              
              <!-- CREATE NESTED FOR REPLIES -->
              {#if comment.replies && comment.replies.length > 0}
                <div class="replies">
                  {#each comment.replies as reply}
                    <div class="reply">
                      <div class="comment-header">
                        <strong>{reply.user}</strong>
                      </div>
                      <div class="comment-body">
                        <p>{reply.text}</p>
                      </div>
                      <div class="comment-footer">
                        <button class="reply-button" on:click={() => startReply(reply.id)}>Reply</button>
                      </div>
                    </div>
                  {/each}
                </div>
              {/if}
            </div>
          {/each}
        {/if}
      </div>
    </div>
  </div>
{/if}

<style>

.comments-panel {
  position: fixed;
  top: 0; right: 0;
  width: 400px;
  height: 100vh;
  background: white;
  display: flex;
  flex-direction: column;
}

.comments-header, 
.comment-form {
  padding: 10px 15px;
  background-color: #f0f0f0;
  border-radius: 8px 8px 0 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.comments-header {
  background-color: #f0f0f0;
  border-radius: 0;
}

.comments-header h2 {
  margin: 0;
  font-size: 20px;
  flex-grow: 1;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  color: #5e6061;
}

.comments-content {
  padding: 15px;
  flex: 1;
  overflow-y: auto;
  background: #fafafa;
}

.comment-form {
  flex-direction: column;
  background-color: #f9f9f9;
  margin-bottom: 20px;
}

.comment-form h3 {
  margin: 0 0 15px 0;
  font-size: 18px;
  align-self: flex-start;
}

.reply-info {
  background-color: #e8f0f8;
  border-radius: 4px;
  padding: 8px;
  margin-bottom: 10px;
  font-size: 14px;
}

.comment-form input,
.comment-form textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

.comment-form textarea {
  min-height: 100px;
  resize: vertical;
}

.submit-button {
  align-self: flex-start;
  background-color: #5e6061;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  font-size: 14px;
}

.comments-list {
  margin-top: 20px;
}

.no-comments {
  text-align: center;
  color: #777;
  font-style: italic;
}

.comment, .reply {
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  padding: 15px;
  margin-bottom: 15px;
}

.reply {
  background-color: #f8f8f8;
  margin-left: 20px;
  border-left: 4px solid #e0e0e0;
  padding-left: 15px;
}

.comment-header, .comment-footer {
  margin-bottom: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comment-body p {
  margin: 0;
  line-height: 1.4;
}

.reply-button {
  background: transparent;
  border: 1px solid #5e6061;
  color: #5e6061;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 12px;
}
</style>