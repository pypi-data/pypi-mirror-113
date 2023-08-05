Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_document_title_1 = tslib_1.__importDefault(require("react-document-title"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var AsyncView = /** @class */ (function (_super) {
    tslib_1.__extends(AsyncView, _super);
    function AsyncView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AsyncView.prototype.getTitle = function () {
        return '';
    };
    AsyncView.prototype.render = function () {
        var title = this.getTitle();
        return (<react_document_title_1.default title={(title ? title + " - " : '') + "Sentry"}>
        {this.renderComponent()}
      </react_document_title_1.default>);
    };
    return AsyncView;
}(asyncComponent_1.default));
exports.default = AsyncView;
//# sourceMappingURL=asyncView.jsx.map