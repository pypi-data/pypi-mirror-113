Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var prop_types_1 = tslib_1.__importDefault(require("prop-types"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var callIfFunction_1 = require("app/utils/callIfFunction");
var parseLinkHeader_1 = tslib_1.__importDefault(require("app/utils/parseLinkHeader"));
var defaultProps = {
    size: 'small',
    disabled: false,
    onCursor: function (cursor, path, query, _direction) {
        react_router_1.browserHistory.push({
            pathname: path,
            query: tslib_1.__assign(tslib_1.__assign({}, query), { cursor: cursor }),
        });
    },
};
var Pagination = /** @class */ (function (_super) {
    tslib_1.__extends(Pagination, _super);
    function Pagination() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Pagination.prototype.render = function () {
        var _a = this.props, className = _a.className, onCursor = _a.onCursor, pageLinks = _a.pageLinks, size = _a.size, caption = _a.caption, disabled = _a.disabled;
        if (!pageLinks) {
            return null;
        }
        var location = this.context.location;
        var path = this.props.to || location.pathname;
        var query = location.query;
        var links = parseLinkHeader_1.default(pageLinks);
        var previousDisabled = disabled || links.previous.results === false;
        var nextDisabled = disabled || links.next.results === false;
        return (<Wrapper className={className}>
        {caption}
        <buttonBar_1.default merged>
          <button_1.default icon={<icons_1.IconChevron direction="left" size="sm"/>} aria-label={locale_1.t('Previous')} size={size} disabled={previousDisabled} onClick={function () {
                callIfFunction_1.callIfFunction(onCursor, links.previous.cursor, path, query, -1);
            }}/>
          <button_1.default icon={<icons_1.IconChevron direction="right" size="sm"/>} aria-label={locale_1.t('Next')} size={size} disabled={nextDisabled} onClick={function () {
                callIfFunction_1.callIfFunction(onCursor, links.next.cursor, path, query, 1);
            }}/>
        </buttonBar_1.default>
      </Wrapper>);
    };
    Pagination.contextTypes = {
        location: prop_types_1.default.object,
    };
    Pagination.defaultProps = defaultProps;
    return Pagination;
}(react_1.Component));
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n  margin: ", " 0 0 0;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n  margin: ", " 0 0 0;\n"])), space_1.default(3));
exports.default = Pagination;
var templateObject_1;
//# sourceMappingURL=index.jsx.map