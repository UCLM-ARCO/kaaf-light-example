(in-context {general})

(new-type {resource} {thing})
(new-is-a {information} {resource}) ;; already in the KB core

(new-is-a {light} {resource})
(new-is-a {motion event} {information})
(new-is-a {occupied room} {information})

(new-type-role {provider} {thing} {thing})
(new-type-role {location} {thing} {place})

(new-relation {indicate} ;; A indicates B. Ex: motion event indicates occupied room
        :a-inst-of {information}
        :b-inst-of {information}
        :c-inst-of {location})
    
(new-relation {require}  ;; A requires B. Ex: occupied room requires light
        :a-inst-of {information}
        :b-inst-of {resource}
        :c-inst-of {location})

;; ---------- Occupation
(new-indv {motion sensor:location} {place})
(x-is-the-y-of-z {motion sensor} {provider} {motion event})
(x-is-the-y-of-z {motion sensor:location} {location} {motion sensor})
(new-statement {motion event} {indicate} {occupied room} :c (the-x-of-y {location} (the-x-role-of-y {provider} {motion event})))

(new-indv {occupied room:location} {place})
(x-is-the-y-of-z {occupied room} {occupation status} {occupied room:location})
(new-statement {occupied room} {require} {light} :c {occupied room:location})

;; ---------- Illumination
(x-is-the-y-of-z {bulb} {provider} {light})

(new-context {day} {general})
(new-context {night} {general})

(in-context {day})
(x-is-the-y-of-z {window} {provider} {light})
(in-context {night})
(x-is-not-the-y-of-z {window} {provider} {light})
(in-context {general})


