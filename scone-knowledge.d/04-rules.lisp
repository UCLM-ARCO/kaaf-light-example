(in-context {general})

(new-type {resource} {thing})
(new-type {provider} {thing})

(new-is-a {device} {provider})
(new-is-a {light} {resource})

(new-relation {provide} 
        :a-inst-of {provider}
        :b-inst-of {resource})

(new-relation {entail}
        :a-inst-of {thing}
        :b-inst-of {thing}
        :c-inst-of {thing}
        :transitive t)

(new-relation {require}
        :parent {entail}
        :b-inst-of {resource})

;; ---------- Occupation
(new-statement {motion sensor} {provide} {motion event})
(new-statement {motion event} {entail} {inhabited room})

;; ---------- Illumination
(new-statement {lamp} {provide} {light})

(new-statement {inhabited room} {require} {light})
(new-not-statement {uninhabited room} {require} {light})

(new-context {day} {general})
(new-context {night} {general})

(in-context {day})
(new-statement {window} {provide} {light})
(in-context {night})
(new-not-statement {window} {provide} {light})
(in-context {general})


