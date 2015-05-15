/*
 * Copyright (C) 2008 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package targets;

import dalvik.annotation.VirtualTestTarget;

/**
 * @hide
 */
public interface KeyGenerator {
    /**
     * @hide
     */
    abstract class Internal {
        protected Internal() {
        }
    }

    @VirtualTestTarget
    static abstract class AES extends Internal {
        protected abstract void method();
    }

    @VirtualTestTarget
    static abstract class DES extends Internal {
        protected abstract void method();
    }

    @VirtualTestTarget
    static abstract class DESede extends Internal {
        protected abstract void method();
    }

    @VirtualTestTarget
    static abstract class HMACMD5 extends Internal {
        protected abstract void method();
    }

    @VirtualTestTarget
    static abstract class HMACSHA1 extends Internal {
        protected abstract void method();
    }

    @VirtualTestTarget
    static abstract class HMACSHA256 extends Internal {
        protected abstract void method();
    }

    @VirtualTestTarget
    static abstract class HMACSHA384 extends Internal {
        protected abstract void method();
    }

    @VirtualTestTarget
    static abstract class HMACSHA512 extends Internal {
        protected abstract void method();
    }
}
