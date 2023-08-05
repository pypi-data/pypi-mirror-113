Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
/**
 * Hook that updates when a media query result changes
 */
function useMedia(query) {
    if (!window.matchMedia) {
        return false;
    }
    var _a = tslib_1.__read(react_1.useState(function () { return window.matchMedia(query).matches; }), 2), state = _a[0], setState = _a[1];
    react_1.useEffect(function () {
        var mounted = true;
        var mql = window.matchMedia(query);
        var onChange = function () {
            if (!mounted) {
                return;
            }
            setState(!!mql.matches);
        };
        mql.addListener(onChange);
        setState(mql.matches);
        return function () {
            mounted = false;
            mql.removeListener(onChange);
        };
    }, [query]);
    return state;
}
exports.default = useMedia;
//# sourceMappingURL=useMedia.jsx.map