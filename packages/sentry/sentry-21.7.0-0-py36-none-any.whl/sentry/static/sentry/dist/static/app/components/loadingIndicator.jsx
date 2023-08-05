Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@sentry/react");
var classnames_1 = tslib_1.__importDefault(require("classnames"));
var sentry_loader_svg_1 = tslib_1.__importDefault(require("sentry-images/sentry-loader.svg"));
function renderLogoSpinner() {
    return <img src={sentry_loader_svg_1.default}/>;
}
function LoadingIndicator(props) {
    var hideMessage = props.hideMessage, mini = props.mini, triangle = props.triangle, overlay = props.overlay, dark = props.dark, children = props.children, finished = props.finished, className = props.className, style = props.style, relative = props.relative, size = props.size, hideSpinner = props.hideSpinner;
    var cx = classnames_1.default(className, {
        overlay: overlay,
        dark: dark,
        loading: true,
        mini: mini,
        triangle: triangle,
    });
    var loadingCx = classnames_1.default({
        relative: relative,
        'loading-indicator': true,
        'load-complete': finished,
    });
    var loadingStyle = {};
    if (size) {
        loadingStyle = {
            width: size,
            height: size,
        };
    }
    return (<div className={cx} style={style} data-test-id="loading-indicator">
      {!hideSpinner && (<div className={loadingCx} style={loadingStyle}>
          {triangle && renderLogoSpinner()}
          {finished ? <div className="checkmark draw" style={style}/> : null}
        </div>)}
      {!hideMessage && <div className="loading-message">{children}</div>}
    </div>);
}
exports.default = react_1.withProfiler(LoadingIndicator, {
    includeUpdates: false,
});
//# sourceMappingURL=loadingIndicator.jsx.map