Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_document_title_1 = tslib_1.__importDefault(require("react-document-title"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var notFound_1 = tslib_1.__importDefault(require("app/components/errors/notFound"));
var footer_1 = tslib_1.__importDefault(require("app/components/footer"));
var sidebar_1 = tslib_1.__importDefault(require("app/components/sidebar"));
var RouteNotFound = /** @class */ (function (_super) {
    tslib_1.__extends(RouteNotFound, _super);
    function RouteNotFound() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getTitle = function () { return 'Page Not Found'; };
        return _this;
    }
    RouteNotFound.prototype.componentDidMount = function () {
        Sentry.withScope(function (scope) {
            scope.setFingerprint(['RouteNotFound']);
            Sentry.captureException(new Error('Route not found'));
        });
    };
    RouteNotFound.prototype.render = function () {
        // TODO(dcramer): show additional resource links
        return (<react_document_title_1.default title={this.getTitle()}>
        <div className="app">
          <sidebar_1.default location={this.props.location}/>
          <div className="container">
            <div className="content">
              <section className="body">
                <notFound_1.default />
              </section>
            </div>
          </div>
          <footer_1.default />
        </div>
      </react_document_title_1.default>);
    };
    return RouteNotFound;
}(react_1.Component));
exports.default = RouteNotFound;
//# sourceMappingURL=routeNotFound.jsx.map