---
name: 论文写作
description: 提高ML/CV/NLP风格论文的写作质量，确保章节结构清晰、段落流畅，并面向评审人进行展示。在撰写或修订摘要、引言、相关工作、方法、实验或结论时使用；润色图表；检查论点与支持材料的一致性；或在提交前进行自我审查。
---

# Research Paper Writing

## Overview

Use this skill to rewrite a research paper into a reviewer-friendly, high-clarity draft.
Prioritize first-impression quality (figures/tables/layout), logical flow, and evidence-backed claims.

## Core Workflow

1. Clarify the paper story before sentence-level edits.
2. Use section-specific guidance in `references/`.
3. Rewrite paragraph-by-paragraph with one message per paragraph.
4. Run reverse outlining after writing each section.
5. Check every major claim in Abstract/Introduction against experimental evidence.
6. Run final-paper adversarial review with `references/paper-review.md`.

## Global Principles

1. Keep one paragraph for one message only.
2. State the paragraph message in the first sentence.
3. Make nouns self-contained; define new terms before reusing them.
4. Maintain sentence-to-sentence flow (cause, contrast, consequence, or refinement).
5. Iterate with adversarial self-review: read as a skeptical reviewer.
6. Treat visual quality as core content, not decoration.
7. Use a clean teaser and pipeline figure.
8. Use readable, minimal-ink tables.
9. Keep formatting consistent and tidy.

## Paragraph Clarity Check (Important)

Use this quick test whenever the user asks whether a paragraph "flows" or is clear.

1. Read as an external reader:
   - Does this paragraph have one explicit message?
   - Does the first sentence state what this paragraph will do?
   - Are all key nouns/terms readable without hidden context?
   - Does each sentence connect to the previous one with a clear relation (cause, contrast, consequence, refinement, example)?
2. Run reverse outlining for the current section:
   - Write down thesis/main claim.
   - Write down each paragraph topic sentence.
   - Write down the evidence/explanation points under each paragraph.
   - Check mapping: topic sentence -> thesis, and evidence -> topic sentence.
   - Revise or remove any paragraph that cannot be mapped cleanly.
3. If flow is still weak, add temporary section headers and explicit transition phrases during revision, then remove unnecessary headers before finalizing.

Source reference for this check:

- `references/does-my-writing-flow-source.md`

## Section Guides

Load only the needed section file:

- Introduction: `references/introduction.md`
- Abstract: `references/abstract.md`
- Related Work: `references/related-work.md`
- Method: `references/method.md`
- Experiments: `references/experiments.md`
- Conclusion: `references/conclusion.md`
- Paper review (Paper Rview): `references/paper-review.md`
- Paragraph clarity source: `references/does-my-writing-flow-source.md`
- Example bank index: `references/examples/index.md`

## Paper Review Core Points

Use `references/paper-review.md` for the full checklist and workflow.

1. Add an end-of-draft self-review question list in five dimensions:
   - contribution,
   - writing clarity,
   - experimental strength,
   - evaluation completeness,
   - method design soundness.
2. Treat claim-evidence alignment as a hard constraint, especially for Abstract and Introduction.
3. Perform adversarial writing: review as a skeptical reviewer and resolve every high-risk question.
4. Revise until major rejection risks are explicitly addressed.

## Execution Rules

1. Build a mini-outline before drafting prose.
2. For each subsection, explicitly include motivation, design, and technical advantage when applicable.
3. Avoid writing style that looks like incremental patching of a naive baseline.
4. Keep terminology stable across the full paper.
5. If a claim cannot be supported by results, weaken or remove the claim.
6. Before finalizing, append and answer a five-dimension self-review question list, then revise the paper based on unresolved items.
7. Do not load all section references (Introduction/Abstract/Related Work/Method/Experiments/Conclusion) at once; load only the specific section guide needed for the current edit target.

## Output Contract

When asked to rewrite or draft sections, return:

1. A compact section outline (3-7 bullets).
2. Revised paragraphs with explicit paragraph roles (opening/challenge/method/advantage/evidence/limitation).
3. A short self-review checklist covering clarity, flow, terminology consistency, unsupported claims, and missing evidence.
4. A claim-evidence map for each major claim in the revised text using `Claim: ... | Evidence: ... | Status: supported/needs evidence`.

---

## 参考资料：references/abstract.md

# Abstract Writing Guide

## Goal

Write a strong abstract by doing three things repeatedly:

1. Think through the abstract logic first.
2. Follow one template (Version 1/2/3 below).
3. Revise the abstract many times.

## Pre-Writing Questions (Important)

Answer these before writing:

1. What technical problem do we solve, and why is there no well-established solution? (important)
2. What is our technical contribution?
3. Why can our method work in essence?
4. What technical advantage and new insight do we provide? (important)

## Version 1: Challenge -> Contribution

Introduce the technical challenge, then use one to two sentences to present the technical contribution that solves the challenge.

### Structure

1. Task.
2. Technical challenge for previous methods.
3. One to two sentences introducing the technical contribution for solving the challenge.
4. Benefits of the technical contribution.
5. Experiment summary.

### Expert Notes

1. Discuss previous work around the technical challenge that we actually solve.
2. For the contribution sentence(s), usually mention the technical term/name only; do not explain every detailed step.
3. The technical term must be easy to understand; readers should not feel a jump.
4. This ability is very important for writing a good abstract.

Version 1 local cite:

1. `references/examples/abstract/template-a.md`

## Version 2: Challenge -> Insight -> Contribution

Introduce the technical challenge, then use one to two sentences to present the insight for solving the challenge, and then one sentence to present the technical contribution that implements this insight.

### Structure

1. Task.
2. Technical challenge for previous methods.
3. One sentence introducing the insight for solving the challenge.
4. One to two sentences introducing the technical contribution that implements the insight.
5. Benefits of technical novelty.
6. Experiment summary.

### Expert Notes

1. Discuss previous work around the technical challenge that we actually solve.
2. Introduce the insight in one clear sentence.
3. For the implementation sentence(s), usually mention the technical term/name only; do not explain every detailed step.
4. The technical term must be easy to understand; do not create a jump in reading.
5. This ability is very important for writing a good abstract.

Version 2 local cite:

1. `references/examples/abstract/template-b.md`

## Version 3: Multiple Contributions

Version 3: When there are multiple technical contributions, describe each contribution together with its technical advantage.

### Structure

1. Task.
2. If needed, one contrast sentence about prior methods.
3. Contribution sentence 1 + technical advantage.
4. Contribution sentence 2 + technical advantage.
5. Contribution sentence 3 + technical advantage.
6. Experiment summary.

### Expert Notes

1. When there are multiple technical contributions, describe each contribution together with its technical advantage.
2. The ability to express "contribution + advantage" in one sentence is very important for writing a good abstract.

Version 3 local cite:

1. `references/examples/abstract/template-c.md`

## Example Bank

1. `references/examples/abstract-examples.md`
2. `references/examples/abstract/template-a.md`
3. `references/examples/abstract/template-b.md`
4. `references/examples/abstract/template-c.md`

## Abstract Quality Checklist

1. Can a reader identify task, challenge, insight/contribution, and results in one pass?
2. Are all major claims supported by experiments?
3. Are technical names self-contained and readable?
4. Is there any sentence that mixes too many messages?

---

## 参考资料：references/conclusion.md

# Conclusion Writing Guide

## Goal

Close the paper with clear takeaways and credible limitations.

## Structure

1. Restate solved problem and core technical idea.
2. Summarize strongest evidence from experiments.
3. State practical impact or new insight.
4. Add limitation paragraph.
5. End with concrete future direction.

## Limitation Guidance

Prefer limitations tied to task goal/setting boundaries, for example:

1. Data regime limitation (e.g., only short sequences).
2. Assumption limitation (e.g., controlled viewpoints only).
3. Deployment scope limitation (e.g., specific sensor setup).

Avoid framing conclusion around fixable implementation flaws unless they critically define your method's scope.

## Distinguish Limitation Types

1. Technical defect: underperforms strong baselines on key metrics or causes unacceptable tradeoff.
2. Scope limitation: bounded by current task setting and still competitive vs. current SOTA.

## Template

1. This paper addresses [problem] by proposing [method].
2. The key idea is [core insight], which enables [main benefit].
3. Experiments show [main gains] across [datasets/settings].
4. A current limitation is [scope boundary], and extending to [future setting] is an important next step.

---

## 参考资料：references/does-my-writing-flow-source.md

# Does My Writing Flow? 

Note: This file stores the source content extracted from the PDF, with light formatting cleanup for Markdown readability.

## Original Content

### Does My Writing Flow?

One of the most frequent questions writers ask themselves or others is "does my writing flow?" Other variations of this question include "does this make sense?" and "can you understand what I am saying?" The term flow is a vague term that writers use when describing some concern of clarity, coherence, or conciseness. However vague this term may be, writers know it is a very important concern about their work. If you find yourself concerned about the flow of your writing, then here are some strategies to improve it.

1. Pretend you are the reader of your paper.

   - Often when we write, our work makes sense to us because we are the ones who create it. However, at a certain point in the writing process, our writing may become unclear even to us. When we as authors begin to lose sight of our paper's train of thought, other readers are sure to be confused as well.
   - By looking at your paper from the perspective of a reader, you are checking and making sure your writing is clear to someone who might not be as informed of the paper's topic as you are.
   - Some questions you might ask to place yourself in the reader's shoes are:
     1. Would my classmates be able to understand the level of vocabulary I am using?
     2. How do my body paragraphs connect back to my thesis, and is the connection easy to see?
     3. Would someone not in my class understand what I am trying to say?
2. Reverse-outlining

   - Outlining is not only a great pre-writing exercise, but it also can serve as a great post-writing tool. Reverse-outlining means just what it sounds like. It breaks down an already written essay into its basic parts (such as thesis statement, topic-sentences, and the points of proof/explanation used within your body paragraphs), and it allows a writer to see how well topic sentences and paragraphs fit into an essay.
   - Here is how to reverse outline:
     1. Write down the thesis statement.
     2. Write down each topic sentence of each body paragraph.
     3. Also write down the main points of evidence or explanation used within your body paragraphs.
     4. Check every topic sentence and make sure it is clearly related to a part of your thesis statement.
     5. Check all points of proof/explanation and make sure they pertain to the topic of the paragraph and provide adequate support.
     6. If there is a topic sentence that does not clearly relate to the thesis statement, then either revise it and its supporting points of proof/explanation or take it out entirely.
   - If it is easy to write a reverse outline, then it's a good sign that your paper is well-organized. If you have a hard time creating a reverse outline, then your thesis statement and topic-sentences might be unclear.
3. Add headings and sections to your paper.

   - If you are not up to making a complete outline (or if you are not very good at outlining - lots of people aren't), then no need to feel bad. You can add headings and sections to your paper. This method achieves a similar effect to reverse outlining.
   - By splitting a paper into sections and sub-sections with headings, the paper is telling the reader what each part is all about.
   - For most papers, headings are not necessary. However, you can still make use of them as a tool for drafting and revision. By adding headers to the different sections of a paper, you can easily begin to see the main parts of your paper and how they work together.
4. Use transitions or "flow" keywords.

   - Using appropriate transition words improves the flow of your paper. These words act as guide posts, indicating the relationship between thoughts, sentences, or paragraphs. You can always make your essay flow better by adding appropriate transitional words and phrases.
   - Transitional words and phrases:
     - To show causes and effects: accordingly, as a result, because, consequently, hence, so, then, therefore, thus
     - To show comparison: also, in the same way, likewise, similarly
     - To show contrasts or exceptions: although, but, even though, however, in contrast, instead, nevertheless, nonetheless, on the contrary, on the one hand ... on the other hand, still, yet
     - To show examples: even, for example, for instance, indeed, in fact, of course, such as
     - To show place or position: above, adjacent to, below, beyond, finally, furthermore, last, moreover, next, too
     - To show time: after, as soon as, at first, at the same time, before, eventually, finally, immediately, later, meanwhile, next, simultaneously, so far, soon, then, thereafter
     - To signal a summary or conclusion: as a result, as we have seen, finally, in a word, in any event, in brief, in conclusion, in other words, in short, in the end, in a final analysis, on the whole, therefore, thus, to summarize

---

## 参考资料：references/examples/abstract-examples.md

# Abstract Examples Index

All abstract example cites should point to the local files below.

1. Version 1 (Challenge -> Contribution)
`Version 1: Introduce the technical challenge, then use one to two sentences to present the technical contribution that solves the challenge.`
`references/examples/abstract/template-a.md`
2. Version 2 (Challenge -> Insight -> Contribution)
`Version 2: Introduce the technical challenge, then use one to two sentences to present the insight for solving the challenge, and then one sentence to present the technical contribution that implements this insight. (Personally recommended.)`
`references/examples/abstract/template-b.md`
3. Version 3 (Multiple Contributions)
`Version 3: When there are multiple technical contributions, describe each contribution together with its technical advantage.`
`references/examples/abstract/template-c.md`

---

## 参考资料：references/examples/abstract/template-a.md

# Abstract Template A Examples (Challenge -> Contribution)

Source scope: your original notes, "Version 1".

```latex
\section{Abstract}
% Task
% Technical challenge for previous methods (discuss around the technical challenge that we solved)
% Introduce the technical contribution for solving the challenge in one to two sentences (usually mention the technical term/name only, without describing every detailed step. The term should be easy to understand and should not create a jump in reading. This ability is very important for writing a good abstract.)
% Introduce the benefits of the technical contribution
% Experiment
```

## Reusable skeleton

1. `[Task sentence]`
2. `However, previous methods suffer from [technical challenge].`
3. `To solve this challenge, we propose [technical contribution name].`
4. `[One more contribution sentence if needed].`
5. `This contribution brings [technical benefit].`
6. `Experiments show [main result].`

---

## 参考资料：references/examples/abstract/template-b.md

# Abstract Template B Examples (Challenge -> Insight -> Contribution)

```latex
\section{Abstract}
% Task
%% Example 1: In recent years, generative models have undergone significant advancement due to the success of diffusion models.
%% Example 2: This paper addresses the challenge of novel view synthesis for a human performer from a very sparse set of camera views.

% Technical challenge for previous methods (discuss around the technical challenge that we solved)
%% Example 1: The success of these models is often attributed to their use of guidance techniques, such as classifier and classifier-free methods, which provides effective mechanisms to tradeoff between fidelity and diversity. However, these methods are not capable of guiding a generated image to be aware of its geometric configuration, e.g., depth, which hinders the application of diffusion models to areas that require a certain level of depth awareness.
%% Example 2: Some recent works have shown that learning implicit neural representations of 3D scenes achieves remarkable view synthesis quality given dense input views. However, the representation learning will be ill-posed if the views are highly sparse.

% Introduce the insight for solving the challenge in one sentence
%% Example 1: To address this limitation, we propose a novel guidance approach for diffusion models that uses estimated depth information derived from the rich intermediate representations of diffusion models.
%% Example 2: To solve this ill-posed problem, our key idea is to integrate observations over video frames.

% Introduce the technical contribution that implements the insight in one to two sentences (usually mention the technical term/name only, without describing every detailed step. The term should be easy to understand and should not create a jump in reading. This ability is very important for writing a good abstract.)
%% Example 1: To do this, we first present a label-efficient depth estimation framework using the internal representations of diffusion models. At the sampling phase, we utilize two guidance techniques to self-condition the generated image using the estimated depth map, the first of which uses pseudo-labeling, and the subsequent one uses a depth-domain diffusion prior.
%% Example 2: To this end, we propose Neural Body, a new human body representation which assumes that the learned neural representations at different frames share the same set of latent codes anchored to a deformable mesh

% Introduce the benefits of technical novelty
%% Example 2: so that the observations across frames can be naturally integrated. The deformable mesh also provides geometric guidance for the network to learn 3D representations more efficiently.

% Experiment
```

## Given example pattern 2

1. `This paper addresses the challenge of novel view synthesis for a human performer from a very sparse set of camera views.`
2. `... representation learning will be ill-posed if the views are highly sparse.`
3. `To solve this ill-posed problem, our key idea is to integrate observations over video frames.`
4. `To this end, we propose Neural Body ...`
5. `... observations across frames can be naturally integrated ... provides geometric guidance ...`
6. `Experiments show [main result].`

---

## 参考资料：references/examples/abstract/template-c.md

# Abstract Template C Examples (Multiple Contributions)

```latex
% Task
%% This paper introduces a novel contour-based approach named deep snake for real-time instance segmentation.

%% Unlike some recent methods that directly regress the coordinates of the object boundary points from an image

% Introduce technical contribution and technical advantage in one sentence (this ability is very important for writing a good abstract.)
%% deep snake uses a neural network to iteratively deform an initial contour to match the object boundary, which implements the classic idea of snake algorithms with a learning-based approach.

% Introduce technical contribution and technical advantage in one sentence
%% For structured feature learning on the contour, we propose to use circular convolution in deep snake, which better exploits the cycle-graph structure of a contour compared against generic graph convolution.

% Introduce technical contribution and technical advantage in one sentence
%% Based on deep snake, we develop a two-stage pipeline for instance segmentation: initial contour proposal and contour deformation, which can handle errors in object localization.

% Experiment
```

## Given example pattern (Deep Snake style from your text)

1. `This paper introduces a novel contour-based approach named deep snake for real-time instance segmentation.`
2. `Unlike some recent methods that directly regress the coordinates of the object boundary points from an image ...`
3. `deep snake uses a neural network to iteratively deform an initial contour ...`
4. `For structured feature learning on the contour, we propose circular convolution ...`
5. `Based on deep snake, we develop a two-stage pipeline ...`
6. `Experiments show [main result].`

---

## 参考资料：references/examples/index.md

# Example Bank Index

Use this folder for concrete writing patterns and locally organized cite targets.

## Files

1. Abstract examples index: `references/examples/abstract-examples.md`
2. Introduction examples index: `references/examples/introduction-examples.md`
3. Abstract template files: `references/examples/abstract/template-a.md`, `references/examples/abstract/template-b.md`, `references/examples/abstract/template-c.md`
4. Introduction task/application files: `references/examples/introduction/version-1-task-then-application.md`, `references/examples/introduction/version-2-application-first.md`, `references/examples/introduction/version-3-general-to-specific-setting.md`, `references/examples/introduction/version-4-open-with-challenge.md`
5. Introduction technical-challenge files: `references/examples/introduction/technical-challenge-version-1-existing-task.md`, `references/examples/introduction/technical-challenge-version-2-existing-task-insight-backed-by-traditional.md`, `references/examples/introduction/technical-challenge-version-3-novel-task.md`, `references/examples/introduction/novel-task-challenge-decomposition.md`
6. Introduction pipeline files: `references/examples/introduction/pipeline-version-1-one-contribution-multi-advantages.md`, `references/examples/introduction/pipeline-version-2-two-contributions.md`, `references/examples/introduction/pipeline-version-3-new-module-on-existing-pipeline.md`, `references/examples/introduction/pipeline-version-4-observation-driven.md`, `references/examples/introduction/pipeline-not-recommended-abstract-only.md`
7. Method examples index: `references/examples/method-examples.md`
8. Method detail files: `references/examples/method/pre-writing-questions.md`, `references/examples/method/module-triad-neural-body.md`, `references/examples/method/neural-body-annotated-figure-text.md`, `references/examples/method/module-design-instant-ngp.md`, `references/examples/method/module-motivation-patterns.md`, `references/examples/method/section-skeleton.md`, `references/examples/method/overview-template.md`, `references/examples/method/example-of-the-three-elements.md`, `references/examples/method/method-writing-common-issues-note.md`

## Usage

1. Pick one template from a section guide.
2. Open the matching examples file.
3. Reuse the sentence logic, not exact wording.
4. Keep citation links in your notes for traceability.

---

## 参考资料：references/examples/introduction-examples.md

# Introduction Examples Index

All introduction example cites should point to the local files below.

## A. Task and Application Versions

1. Version 1: `references/examples/introduction/version-1-task-then-application.md`
2. Version 2: `references/examples/introduction/version-2-application-first.md`
3. Version 3: `references/examples/introduction/version-3-general-to-specific-setting.md`
4. Version 4: `references/examples/introduction/version-4-open-with-challenge.md`

## B. Technical Challenge Versions

1. Version 1 (existing task): `references/examples/introduction/technical-challenge-version-1-existing-task.md`
2. Version 2 (existing task + traditional insight backing): `references/examples/introduction/technical-challenge-version-2-existing-task-insight-backed-by-traditional.md`
3. Version 3 (novel task): `references/examples/introduction/technical-challenge-version-3-novel-task.md`
4. Novel-task decomposition examples: `references/examples/introduction/novel-task-challenge-decomposition.md`

## C. Pipeline-Introduction Versions

1. Version 1: `references/examples/introduction/pipeline-version-1-one-contribution-multi-advantages.md`
2. Version 2: `references/examples/introduction/pipeline-version-2-two-contributions.md`
3. Version 3: `references/examples/introduction/pipeline-version-3-new-module-on-existing-pipeline.md`
4. Version 4: `references/examples/introduction/pipeline-version-4-observation-driven.md`
5. Not recommended pattern: `references/examples/introduction/pipeline-not-recommended-abstract-only.md`

---

## 参考资料：references/examples/introduction/novel-task-challenge-decomposition.md

# Introduction Novel-Task Challenge Decomposition


`For novel tasks without direct methods, decompose the challenge into clear requirement/challenge points.`

```latex
% To achieve xx goal, several requirements must be satisfied (or several challenges must be handled).
%% Example: In this work, our goal is to build a model that captures such object intrinsics from a single image. This problem is challenging for three reasons.

% Describe point 1
%% Example: First, we only have a single image. This makes our work fundamentally different from existing works on 3D-aware image generation models [8, 9, 27, 28], which typically require a large dataset of thousands of instances for training. In comparison, the single image contains at most a few dozen instances, making the inference problem highly under-constrained.

% Describe point 2
%% Example: Second, these already limited instances may vary significantly in pixel values. This is because they have different poses and illumination conditions, but neither of these factors are annotated or known. We also cannot resort to existing tools for pose estimation based on structure from motion, such as COLMAP [35], because the appearance variations violate the assumptions of epipolar geometry.

% Describe point 3
%% Example: Finally, the object intrinsics we aim to infer are probabilistic, not deterministic: no two roses in the natural world are identical, and we want to capture a distribution of their geometry, texture, and material to exploit the underlying multi-view information.
```

---

## 参考资料：references/examples/introduction/pipeline-not-recommended-abstract-only.md

# Not Recommended: Abstract-Only Method Description in Introduction


`Not recommended: If the method is simple, do not avoid concrete method details in Introduction and only discuss abstract insight to make it look novel.`

Expert note (faithful translation):

1. The craft of this writing template is how to make a simple pipeline look novel.
2. Note: this is not about making the insight look novel, but about making the pipeline steps look novel.
3. In most cases this is not recommended.
4. The better target is to clearly explain how the core contribution is implemented in Introduction.

```latex
% To tackle this problem, we propose a novel 3D GAN training method to generate photo-realistic images irrespective of the viewing angle.

% Introduce key idea
% Our key idea is as follows. To ease the challenging problem of learning photorealistic and multi-view consistent image synthesis, we cast the problem into two subproblems, each of which can be solved more easily.

% Explain why the key idea works, but without concretely discussing the full pipeline (or only discuss abstract benefit)
%% Example: Specifically, we formulate the problem as a combination of two simple discrimination problems, one of which learns to discriminate whether a synthesized image looks real or not, and the other learns to discriminate whether a synthesized image agrees with the camera pose. Unlike the formulations of the previous methods, which try to learn the real image distribution for each pose, or to learn pose estimation, our subproblems are much easier as each of them is analogous to a basic binary classification problem.

% Introduce pipeline modules with new terms but without clearly explaining the full pipeline (or skip concrete pipeline details)
%% Example: Based on this key idea, we propose a dual-branched discriminator, which has two branches for learning photorealism and pose consistency, respectively. As these branches are supervised explicitly for their respective purposes, high-quality images with pose consistency can be produced at each viewing angle, and consequently, the generator creates high-quality images and shapes. (This paragraph does not clearly explain how the pipeline works.)

% Introduce another contribution
%% Example: In addition, we propose a pose-matching loss to give supervision to the discriminator for the pose consistency, by considering a positive pose (i.e., rendering pose or ground truth pose) and a negative pose (i.e., irrelevant pose) for a given image. (This paragraph does not clearly explain how the pipeline works.)

% Explain expected benefit over prior methods
%% Example: For example, the frontal viewpoint is one of the irrelevant poses for a side-view image. As reported in the experiments, this loss helps improve image and shape quality. This can be interpreted as a simplification of a classification problem from a large number of classes into binary, which is composed of positive and negative pairs.
```

---

## 参考资料：references/examples/introduction/pipeline-version-1-one-contribution-multi-advantages.md

# Pipeline Version 1 (One Contribution, Multiple Advantages)


`Version 1: One contribution with multiple advantages, and one teaser figure to present the basic idea.`

```latex
% In this paper, we propose a novel framework …
%% Example: In this paper, we introduce a novel implicit neural representation for dynamic humans, named Neural Body, to solve the challenge of novel view synthesis from sparse views.
In this paper, we propose a novel framework/representation, named [method name] for [xxx task].

% Teaser for basic idea
%% Example: The basic idea is illustrated in Figure 2.
The basic idea is illustrated in [xxx Figure].

% One-sentence key novelty/contribution (very important ability)
%% Example: For the implicit fields at different frames, instead of learning them separately, Neural Body generates them from the same set of latent codes.
Our innovation is in [one sentence for key novelty].

% Method details
%% Example: Specifically, we anchor a set of latent codes to the vertices of a deformable human model (SMPL in this work), namely that their spatial locations vary with the human pose. To obtain the 3D representation at a frame, we first transform the code locations based on the human pose, which can be reliably estimated from sparse camera views. Then, a network is designed to regress the density and color for any 3D point based on these latent codes. Both the latent codes and the network are jointly learned from images of all video frames during the reconstruction.
Specifically, [how it works in detail].

% Advantage 1
%% Example: This model is inspired by the latent variable model in statistics, which enables us to effectively integrate observations at different frames.
In contrast to previous methods, [our advantage].

% Advantage 2
%% Example: Another advantage of the proposed method is that the deformable model provides a geometric prior (rough surface location) to enable more efficient learning of implicit fields.
Another advantage of the proposed method is that [another advantage].
```

---

## 参考资料：references/examples/introduction/pipeline-version-2-two-contributions.md

# Pipeline Version 2 (Two Contributions)


`Version 2: Two contributions, and one teaser figure to present the basic idea.`

```latex
% In this paper, we propose a novel framework …
%% Example: In this paper, we introduce a novel implicit neural representation for dynamic humans, named Neural Body, to solve the challenge of novel view synthesis from sparse views.
In this paper, we propose a novel framework/representation, named [method name] for [xxx task].

% One-sentence key novelty
%% Example: To that end, we propose techniques to represent a given subject with rare token identifiers and fine-tune a pre-trained, diffusion-based text-to-image framework that operates in two steps; generating a low-resolution image from text and subsequently applying super-resolution (SR) diffusion models.
Our innovation is in [one sentence for key novelty].

% Teaser
%% Example: The basic idea is illustrated in Figure 2.
The basic idea is illustrated in [xxx Figure].

% Contribution 1 details
%% Example: We first fine-tune the low-resolution text-to-image model with the input images and text prompts containing a unique identifier followed by the class name of the subject (e.g., “A [V] dog”).
Specifically, [how contribution 1 works].

% Advantage of contribution 1
%% Example: This model is inspired by the latent variable model in statistics, which enables us to effectively integrate observations at different frames.
In contrast to previous methods, [advantage of contribution 1].

% Challenge motivating contribution 2
%% Example: In order to prevent overfitting and language drift [35, 40] that cause the model to associate the class name (e.g., “dog”) with the specific instance
However, [another technical challenge].

% Contribution 2 details
%% Example: we propose an autogenous, class-specific prior preservation loss, which leverages the semantic prior on the class that is embedded in the model, and encourages it to generate diverse instances of the same class as our subject.
Specifically, [how contribution 2 works].
```

---

## 参考资料：references/examples/introduction/pipeline-version-3-new-module-on-existing-pipeline.md

# Pipeline Version 3 (New Module on Existing Pipeline)


`Version 3: Build on a prior pipeline and introduce one new module, with a teaser figure for the basic idea.`

```latex
% In this paper, we propose a learning-based snake algorithm, named deep snake, for real-time instance segmentation.

% Inspired by previous methods [21, 25], deep snake takes an initial contour as input and deforms it by regressing vertex-wise offsets.

% Our innovation is introducing the circular convolution for efficient feature learning on a contour, as illustrated in Figure 1.

% We observe that the contour is a cycle graph that consists of a sequence of vertices connected in a closed cycle. Since every vertex has the same degree equal to two, we can apply the standard 1D convolution on the vertex features.

% Considering that the contour is periodic, deep snake introduces the circular convolution, which indicates that an aperiodic function (1D kernel) is convolved in the standard way with a periodic function (features defined on the contour).

% The kernel of circular convolution encodes not only the feature of each vertex but also the relationship among neighboring vertices. In contrast, the generic GCN performs pooling to aggregate information from neighboring vertices. The kernel function in our circular convolution amounts to a learnable aggregation function, which is more expressive and results in better performance than using a generic GCN, as demonstrated by our experimental results in Section 5.2.
```

---

## 参考资料：references/examples/introduction/pipeline-version-4-observation-driven.md

# Pipeline Version 4 (Observation-Driven Contribution)


`Version 4: Contribution comes from one important observation. Introduce key innovation first, then intuitive observation as motivation, then method details, then benefits.`

```latex
% In this paper, we propose a learning-based snake algorithm, named deep snake, for real-time instance segmentation.

% Our innovation is introducing the circular convolution for efficient feature learning on a contour, as illustrated in Figure 1.

% We observe that the contour is a cycle graph that consists of a sequence of vertices connected in a closed cycle. Since every vertex has the same degree equal to two, we can apply the standard 1D convolution on the vertex features.

% Considering that the contour is periodic, deep snake introduces the circular convolution, which indicates that an aperiodic function (1D kernel) is convolved in the standard way with a periodic function (features defined on the contour).

% The kernel of circular convolution encodes not only the feature of each vertex but also the relationship among neighboring vertices. In contrast, the generic GCN performs pooling to aggregate information from neighboring vertices. The kernel function in our circular convolution amounts to a learnable aggregation function, which is more expressive and results in better performance than using a generic GCN, as demonstrated by our experimental results in Section 5.2.
```

---

## 参考资料：references/examples/introduction/technical-challenge-version-1-existing-task.md

# Technical Challenge Version 1 (Existing Task, Existing Methods)


`Version 1: For existing tasks with existing methods, discuss the challenge chain from traditional methods to recent methods and finally to the challenge we solve.`

```latex
% Discuss general technical challenges of this task (to lead into recent methods)
%% Example 1: This problem is quite challenging from many perspectives, including object detection under severe occlusions, variations in lighting and appearance, and cluttered background objects.
%% Example 2: This problem is particularly challenging due to the inherent ambiguity on acquiring human geometry, materials and motions from images.
This problem is particularly challenging due to several factors, including [xxx reason], [xxx reason], and [xxx reason].

% Briefly introduce one class of traditional methods, then discuss their technical challenge
%% Example: Traditional methods have shown that pose estimation can be achieved by establishing the correspondences between an object image and the object model.
To overcome these challenges, traditional methods [how they work], [what they achieve].

%% Example: They rely on hand-crafted features, which are not robust to image variations and background clutters.
However, they [technical challenge they face].

% Briefly introduce one class of recent methods 1 (optional), then discuss their challenge
%% Example: Deep learning based methods train end-to-end neural networks that take an image as input and output its corresponding pose.
Recently, [xxx methods] [how they work], [what they achieve].

%% Example: However, generalization remains as an issue, as it is unclear that such end-to-end methods learn sufficient feature representations for pose estimation.
However, they [limitation], because [xxx technical reason].

% Briefly introduce one class of recent methods 2, then discuss their challenge (must lead to our solved challenge)
%% Example: Some recent methods use CNNs to first regress 2D keypoints and then compute 6D pose parameters using the Perspective-n-Point (PnP) algorithm. In other words, the detected keypoints serve as an intermediate representation for pose estimation. Such two-stage approaches achieve state-of-the-art performance, thanks to robust detection of keypoints.
To overcome this challenge, [xxx methods] [how they work], [what they achieve].

%% Example: However, these methods have difficulty in tackling occluded and truncated objects, since part of their keypoints are invisible. Although CNNs may predict these unseen keypoints by memorizing similar patterns, generalization remains difficult.
However, they [limitation], because [xxx technical reason].
```

---

## 参考资料：references/examples/introduction/technical-challenge-version-2-existing-task-insight-backed-by-traditional.md

# Technical Challenge Version 2 (Existing Task, Insight Backed by Traditional Methods)


`Version 2: For existing tasks, if our technical insight was used in traditional methods, discuss that line to provide conceptual backing.`

```latex
% Introduce one class of traditional/recent methods and discuss their technical challenge (to lead to our insight)
%% Example (Deep Snake): Most of the state-of-the-art instance segmentation methods perform pixel-wise segmentation within a bounding box given by an object detector.
%% Example (ManhattanSDF): Given input images, traditional methods generally estimate the depth map for each image based on the multi-view stereo (MVS) algorithms and then fuse estimated depth maps into 3D models.
Traditional/recent methods [how they work], [what they achieve].

%% Example (Deep Snake): They may be sensitive to the inaccurate bounding box. Moreover, representing an object shape as dense binary pixels generally results in costly post-processing.
%% Example (ManhattanSDF): Although these methods achieve successful reconstruction in most cases, they have difficulty in handling low-textured regions, e.g., floors and walls of indoor scenes, due to the unreliable stereo matching in these regions.
However, they [limitation], because [xxx technical reason].

% Discuss traditional methods that used an insight similar to ours (implicitly backing our idea)
%% Example (Deep Snake): An alternative shape representation is the object contour, which is a set of vertices along the object silhouette. In contrast to pixel-based representation, a contour is not limited within a bounding box and has fewer parameters. Such a contour-based representation has long been used in image segmentation since the seminal work by Kass et al., which is well known as snakes or active contours.
%% Example (ManhattanSDF): To improve the reconstruction of low-textured regions, a typical approach is leveraging the planar prior of manmade scenes, which has long been explored in literature. A renowned example is the Manhattanworld assumption, i.e., the surfaces of man-made scenes should be aligned with three dominant directions.
To overcome this problem, a typical approach is [xxx insight], which has long been explored in literature.

These methods [how they work].

%% Example (Deep Snake): While many variants have been developed in literature, these methods are prone to local optima as the objective functions are handcrafted and typically nonconvex.
%% Example (ManhattanSDF): However, all of them focus on optimizing per-view depth maps instead of the full scene models in 3D space. As a result, depth estimation and plane segmentation could still be inconsistent among views, yielding suboptimal reconstruction quality as demonstrated by our experimental results in Section 5.3.
However, they [limitation], because [xxx technical reason].

% Then discuss newer methods and their remaining challenge (must lead to our solved challenge)
%% Example: There is a recent trend to represent 3D scenes as implicit neural representations and learn the representations from images with differentiable renderers. In particular, [49, 54, 55] use a signed distance field (SDF) to represent the scene and render it into images based on the sphere tracing or volume rendering. Thanks to the well-defined surfaces of SDFs, they recover high-quality 3D geometries from images.
To overcome this challenge, [xxx methods] [how they work], [what they achieve].

%% Example: However, these methods essentially rely on the multi-view photometric consistency to learn the SDFs. So they still suffer from poor performance in low-textured planar regions, as shown in Figure 1, as many plausible solutions may satisfy the photometric constraint in low-textured planar regions.
However, they [limitation], because [xxx technical reason].
```

---

## 参考资料：references/examples/introduction/technical-challenge-version-3-novel-task.md

# Technical Challenge Version 3 (Novel Task)


`Version 3: For novel tasks without direct methods, define the challenge directly and decompose it by requirement/challenge points.`

```latex
% To achieve xx goal, several requirements/challenges must be satisfied.
%% Example: In this work, our goal is to build a model that captures such object intrinsics from a single image. This problem is challenging for three reasons.

% Describe point 1
%% Example: First, we only have a single image. This makes our work fundamentally different from existing works on 3D-aware image generation models [8, 9, 27, 28], which typically require a large dataset of thousands of instances for training. In comparison, the single image contains at most a few dozen instances, making the inference problem highly under-constrained.

% Describe point 2
%% Example: Second, these already limited instances may vary significantly in pixel values. This is because they have different poses and illumination conditions, but neither of these factors are annotated or known. We also cannot resort to existing tools for pose estimation based on structure from motion, such as COLMAP [35], because the appearance variations violate the assumptions of epipolar geometry.

% Describe point 3
%% Example: Finally, the object intrinsics we aim to infer are probabilistic, not deterministic: no two roses in the natural world are identical, and we want to capture a distribution of their geometry, texture, and material to exploit the underlying multi-view information.
```

See also:
1. `references/examples/introduction/novel-task-challenge-decomposition.md`

---

## 参考资料：references/examples/introduction/version-1-task-then-application.md

# Introduction Version 1: Task First, Then Application


`Version 1: If the task is relatively niche, introduce the task first, then introduce applications.`

```latex
% Introduce Task (if the task is very familiar, this part can be skipped)
%% Example: Object pose estimation aims to estimate object's orientation and translation relative to a canonical frame from a single image.
[xxx task] targets at recovering/reconstructing/estimating [xxx output] from [xxx input].

% Introduce Application
%% Example: Accurate pose estimation is essential for a variety of applications such as augmented reality, autonomous driving and robotic manipulation.
[xxx task] has a variety of applications such as [xxx], [xxx], and [xxx].
```

---

## 参考资料：references/examples/introduction/version-2-application-first.md

# Introduction Version 2: Application First


`Version 2: If the task is already familiar to most readers, introduce applications directly.`

```latex
% Introduce Application
%% Example: Accurate pose estimation is essential for a variety of applications such as augmented reality, autonomous driving and robotic manipulation.
[xxx task] has a variety of applications such as [xxx], [xxx], and [xxx].
```

---

## 参考资料：references/examples/introduction/version-3-general-to-specific-setting.md

# Introduction Version 3: General Application -> Specific Setting


`Version 3: Introduce applications of the general task first, then introduce the specific task setting. (Personally recommended when the setting is relatively new.)`

```latex
% Introduce applications of the general task
%% Example: Accurate pose estimation is essential for a variety of applications such as augmented reality, autonomous driving and robotic manipulation.
[xxx task] has a variety of applications such as [xxx], [xxx], and [xxx].

% Introduce the specific task setting
%% Example: This paper focuses on the specific setting of recovering the 6DoF pose of an object, i.e., rotation and translation in 3D, from a single RGB image of that object.
This paper focuses on the specific setting of recovering/reconstructing/estimating [xxx output] from [xxx input].
```

---

## 参考资料：references/examples/introduction/version-4-open-with-challenge.md

# Introduction Version 4: Open with Application and Challenge


`Version 4: If the task is familiar, introduce applications directly and expose the target technical challenge in the opening paragraph via previous methods.`

Expert notes (faithful translation):

1. It is often good if the opening paragraph already states what we want to solve.
2. But this style requires suitable conditions and is less common.
3. Usually, several prior-method paragraphs are still needed before the target challenge becomes clear.

```latex
% Introduce Application
%% Example 1: Reconstructing 3D scenes from multi-view images is a cornerstone of many applications such as augmented reality, robotics, and autonomous driving.
%% Example 2: Instance segmentation is the cornerstone of many computer vision tasks, such as video analysis, autonomous driving, and robotic grasping, which require both accuracy and efficiency.

% Use previous methods to expose the target technical challenge
%% Example 1: Given input images, traditional methods [43, 44, 59] generally estimate the depth map for each image based on the multi-view stereo (MVS) algorithms and then fuse estimated depth maps into 3D models. Although these methods achieve successful reconstruction in most cases, they have difficulty in handling low-textured regions, e.g., floors and walls of indoor scenes, due to the unreliable stereo matching in these regions.
%% Example 2: Most of the state-of-the-art instance segmentation methods [18, 27, 5, 19] perform pixel-wise segmentation within a bounding box given by an object detector [36], which may be sensitive to the inaccurate bounding box. Moreover, representing an object shape as dense binary pixels generally results in costly post-processing.
```

---

## 参考资料：references/examples/method-examples.md

# Method Examples Index

All method example cites should point to the local files below.

## A. Planning and Writing Workflow

1. Pre-writing questions: `references/examples/method/pre-writing-questions.md`

## B. Module Triad and Module-Level Writing

1. Module triad (Neural Body): `references/examples/method/module-triad-neural-body.md`
2. Neural Body figure text conversion: `references/examples/method/neural-body-annotated-figure-text.md`
3. Module design (Instant-NGP): `references/examples/method/module-design-instant-ngp.md`
4. Module motivation patterns: `references/examples/method/module-motivation-patterns.md`

## C. Section-Level Templates

1. Method section skeleton: `references/examples/method/section-skeleton.md`
2. Overview template: `references/examples/method/overview-template.md`
3. Example of the three elements: `references/examples/method/example-of-the-three-elements.md`

## D. Clarity and Troubleshooting

1. Common issues note: `references/examples/method/method-writing-common-issues-note.md`

---

## 参考资料：references/examples/method/example-of-the-three-elements.md

# Example of the Three Elements

This example uses `%` comments as annotations.  
Each `% ...` annotation explains the paragraph(s) immediately below it.

```latex
\begin{quote}
\textbf{Annotation rule.} In this example, each line starting with \% labels the role of the paragraph(s) directly below it.
\end{quote}

\begin{itemize}
\item Module design (data structure)
\item Motivation of this module
\item Technical advantages of this module
\item Module design (forward process)
\end{itemize}

\subsection{3.1. Structured latent codes}

% Module design: introduce the module's data structure
To control the spatial locations of latent codes with the human pose, we anchor these latent codes to a deformable human body model (SMPL) [38]. SMPL is a skinned vertex-based model, which is defined as a function of shape parameters, pose parameters, and a rigid transformation relative to the SMPL coordinate system. The function outputs a posed 3D mesh with 6890 vertices. Specifically, we define a set of latent codes \( Z = \{z_1, z_2, ..., z_{6890}\} \) on vertices of the SMPL model. For the frame \( t \), SMPL parameters \( S_t \) are estimated from the multi-view images \( \{I_t^c \mid c = 1, ..., N_c\} \) using [26]. The spatial locations of the latent codes are then transformed based on the human pose \( S_t \) for the density and color regression. Figure 3 shows an example. The dimension of latent code \( z \) is set to 16 in our experiments.

% Technical advantages of this module
Similar to the local implicit representations [25, 5, 18], the latent codes are used with a neural network to represent the local geometry and appearance of a human. Anchoring these codes to a deformable model enables us to represent a dynamic human. With the dynamic human representation, we establish a latent variable model that maps the same set of latent codes to the implicit fields of density and color at different frames, which naturally integrates observations at different frames.

\subsection{3.2. Code diffusion}

% Motivation of this module
Figure 3(a) shows the process of code diffusion. The implicit fields assign the density and color to each point in the 3D space, which requires us to query the latent codes at continuous 3D locations. This can be achieved with the trilinear interpolation. However, since the structured latent codes are relatively sparse in the 3D space, directly interpolating the latent codes leads to zero vectors at most 3D points. To solve this problem, we diffuse the latent codes defined on the surface to nearby 3D space.

% Module design: introduce module design by describing the module forward process
Inspired by [65, 56, 49], we choose the SparseConvNet [21] to efficiently process the structured latent codes, whose architecture is described in Table 1. Specifically, based on the SMPL parameters, we compute the 3D bounding box of the human and divide the box into small voxels with voxel size of \( 5mm \times 5mm \times 5mm \). The latent code of a non-empty voxel is the mean of latent codes of SMPL vertices inside this voxel. SparseConvNet utilizes 3D sparse convolutions to process the input volume and output latent code volumes with \( 2\times, 4\times, 8\times, 16\times \) downsampled sizes. With the convolution and downsampling, the input codes are diffused to nearby space. Following [56], for any point in 3D space, we interpolate the latent codes from multi-scale code volumes of network layers 5, 9, 13, 17, and concatenate them into the final latent code. Since the code diffusion should not be affected by the human position and orientation in the world coordinate system, we transform the code locations to the SMPL coordinate system.

For any point \( \mathbf{x} \) in 3D space, we query its latent code from the latent code volume. Specifically, the point \( \mathbf{x} \) is first transformed to the SMPL coordinate system, which aligns the point and the latent code volume in 3D space. Then, the latent code is computed using the trilinear interpolation. For the SMPL parameters \( S_t \), we denote the latent code at point \( \mathbf{x} \) as \( \psi(\mathbf{x}, Z, S_t) \). The code vector is passed into MLP networks to predict the density and color for point \( \mathbf{x} \).

\subsection{3.3. Density and color regression}

Figure 3(b) overviews the regression of density and color for any point in 3D space. The density and color fields are represented by MLP networks. Details of network architectures are described in the supplementary material.

% Module design: introduce module design by describing the module forward process
\textbf{Density model.} For the frame \( t \), the volume density at point \( \mathbf{x} \) is predicted as a function of only the latent code \( \psi(\mathbf{x}, Z, S_t) \), which is defined as:

\[
\sigma_t(\mathbf{x}) = M_{\sigma}(\psi(\mathbf{x}, Z, S_t)),
\tag{1}
\]

where \( M_{\sigma} \) represents an MLP network with four layers.

% Module design: introduce the module's data structure
\textbf{Color model.} Similar to [37, 44], we take both the latent code \( \psi(\mathbf{x}, Z, S_t) \) and the viewing direction \( \mathbf{d} \) as input for the color regression. To model the location-dependent incident light, the color model also takes the spatial location \( \mathbf{x} \) as input. We observe that temporally-varying factors affect the human appearance, such as secondary lighting and self-shadowing. Inspired by the auto-decoder [48], we assign a latent embedding \( \ell_t \) for each video frame \( t \) to encode the temporally-varying factors.

% Module design: introduce module design by describing the module forward process
Specifically, for the frame \( t \), the color at \( \mathbf{x} \) is predicted as a function of the latent code \( \psi(\mathbf{x}, Z, S_t) \), the viewing direction \( \mathbf{d} \), the spatial location \( \mathbf{x} \), and the latent embedding \( \ell_t \). Following [51, 44], we apply the positional encoding to both the viewing direction \( \mathbf{d} \) and the spatial location \( \mathbf{x} \), which enables better learning of high frequency functions. The color model at frame \( t \) is defined as:

\[
c_t(\mathbf{x}) = M_c(\psi(\mathbf{x}, Z, S_t), \gamma_d(\mathbf{d}), \gamma_x(\mathbf{x}), \ell_t),
\tag{2}
\]

where \( M_c \) represents an MLP network with two layers, and \( \gamma_d \) and \( \gamma_x \) are positional encoding functions for viewing direction and spatial location, respectively. We set the dimension of \( \ell_t \) to 128 in experiments.

\subsection{3.4. Volume rendering}

% Module design: introduce module design by describing the module forward process
Given a viewpoint, we utilize the classical volume rendering techniques to render the Neural Body into a 2D image. The pixel colors are estimated via the volume rendering integral equation [27] that accumulates volume densities and colors along the corresponding camera ray. In practice, the integral is approximated using numerical quadrature [41, 44]. Given a pixel, we first compute its camera ray \( \mathbf{r} \) using the camera parameters and sample \( N_k \) points \( \{\mathbf{x}_k\}_{k=1}^{N_k} \) along camera ray \( \mathbf{r} \) between near and far bounds. The scene bounds are estimated based on the SMPL model. Then, Neural Body predicts volume densities and colors at these points. For the video frame \( t \), the rendered color \( \hat{C}_t(\mathbf{r}) \) ...
```

---

## 参考资料：references/examples/method/method-writing-common-issues-note.md

# Method Writing Common Issues (Reference Note)

Original source mentioned in your notes:

1. `Method writing common issues (PDF in your source notes)`

Usage recommendation:

1. Use this reference as a troubleshooting checklist after drafting Method.
2. Prioritize unclear motivation, broken flow, missing implementation details, and inconsistent terms.

---

## 参考资料：references/examples/method/module-design-instant-ngp.md

# Module Design Example 

This example uses `%` comments as annotations.
Each `% ...` annotation explains the paragraph(s) immediately below it.

```latex
\begin{quote}
\textbf{Annotation rule.} In this example, each line starting with \% labels the role of the paragraph(s) directly below it.
\end{quote}

\begin{itemize}
\item Motivation of this module
\item Module design (data structure)
\item Module design (forward process)
\end{itemize}

\section{3 \quad MULTIRESOLUTION HASH ENCODING}

% Motivation of this module
Given a fully connected neural network \(m(y;\Phi)\), we are interested in an encoding of its inputs \(y=\operatorname{enc}(x;\theta)\) that improves the approximation qu
