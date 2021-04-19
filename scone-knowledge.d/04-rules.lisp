(in-context {general})

(new-type {resource} {thing})
(new-type {provider} {thing})

(new-is-a {device} {provider})

;;;;;;;;;;;;;;;;;;;;;;;
;; motion-sensor PROVIDE motion-event
;; motion-event ENTAIL inhabited-room
;; inhabited-room REQUIRE light
;;
;; REQUIRE inherits from ENTAIL
;; REQUIRE implies B have to be provided by the system
;; Does ENTAIL define the rules?
;;;;;;;;;;;;;;;;;;;;;;;

(new-relation {provide}  ;; provider provides a resource. It generates a PROVISION
        :a-inst-of {provider}
        :b-inst-of {resource})

;; FIXME:
;; a better verb for "implication"?
(new-relation {entail} ;; fact A entails B. It generates a IMPLICATION
        :a-inst-of {thing}
        :b-inst-of {thing}
        :c-inst-of {thing}
        :transitive t)

;; FIXME:
;; a better verb for "requires"?
(new-relation {require} ;; fact A requires B. It generates a REQUIREMENT
        :parent {entail}
        :b-inst-of {resource})

;; ---------- Occupation
(new-statement {motion sensor} {provide} {motion event})
(new-statement {motion event} {entail} {inhabited room})

;; ---------- Illumination
;; (new-statement {on light source} {provide} {light})
;; (new-not-statement {off light source} {provide} {light})
(new-statement {lamp} {provide} {light}) ;; relations are not inherited!!

(new-statement {inhabited room} {require} {light})
(new-not-statement {uninhabited room} {require} {light})

(new-context {day} {general})
(new-context {night} {general})

(in-context {day})
(new-statement {window} {provide} {light})
(in-context {night})
(new-not-statement {window} {provide} {light})
(in-context {general})


