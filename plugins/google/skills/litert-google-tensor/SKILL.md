---
name: litert-google-tensor
description: >-
  Compiles LiteRT (.tflite) models ahead-of-time for Google Tensor TPUs
  (Tensor G5 on Pixel 10, Tensor G6 on Pixel 11) locally on Linux x86_64 or
  on Google Colab (--colab on macOS, Windows, or ARM hosts),
  benchmarks them on a USB-attached Pixel with LiteRT's benchmark_model
  (NPU latency, peak memory, TPU tile time, TPU energy, optional CPU baseline),
  and packages compiled models for an Android Gradle app as a Google Play AI
  pack with the Tensor NPU runtime module and a Kotlin loader, applies it to
  the app and verifies it on a Pixel. Use when the
  user asks to compile, AOT-compile, or prepare a .tflite model for the Pixel
  TPU/NPU, check whether a .tflite is already Tensor-compiled, measure
  on-device NPU performance of a compiled model, or package or deploy a
  compiled model into their Android app (or replace the one it ships). Don't
  use for Qualcomm, MediaTek, or Samsung NPUs, GPU-only benchmarking,
  LiteRT-LM or LLM (.litertlm) models, on-device JIT compilation, non-Gradle
  builds, or publishing to Google Play.
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/platform-devices/litert-google-tensor/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/platform-devices/litert-google-tensor/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
