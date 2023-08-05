Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var flatMap_1 = tslib_1.__importDefault(require("lodash/flatMap"));
var uniqBy_1 = tslib_1.__importDefault(require("lodash/uniqBy"));
var commitRow_1 = tslib_1.__importDefault(require("app/components/commitRow"));
var styles_1 = require("app/components/events/styles");
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withCommitters_1 = tslib_1.__importDefault(require("app/utils/withCommitters"));
var EventCause = /** @class */ (function (_super) {
    tslib_1.__extends(EventCause, _super);
    function EventCause() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            expanded: false,
        };
        return _this;
    }
    EventCause.prototype.getUniqueCommitsWithAuthors = function () {
        var committers = this.props.committers;
        // Get a list of commits with author information attached
        var commitsWithAuthors = flatMap_1.default(committers, function (_a) {
            var commits = _a.commits, author = _a.author;
            return commits.map(function (commit) { return (tslib_1.__assign(tslib_1.__assign({}, commit), { author: author })); });
        });
        // Remove duplicate commits
        var uniqueCommitsWithAuthors = uniqBy_1.default(commitsWithAuthors, function (commit) { return commit.id; });
        return uniqueCommitsWithAuthors;
    };
    EventCause.prototype.render = function () {
        var _this = this;
        var committers = this.props.committers;
        var expanded = this.state.expanded;
        if (!(committers === null || committers === void 0 ? void 0 : committers.length)) {
            return null;
        }
        var commits = this.getUniqueCommitsWithAuthors();
        return (<styles_1.DataSection>
        <styles_1.CauseHeader>
          <h3>
            {locale_1.t('Suspect Commits')} ({commits.length})
          </h3>
          {commits.length > 1 && (<ExpandButton onClick={function () { return _this.setState({ expanded: !expanded }); }}>
              {expanded ? (<react_1.Fragment>
                  {locale_1.t('Show less')} <icons_1.IconSubtract isCircled size="md"/>
                </react_1.Fragment>) : (<react_1.Fragment>
                  {locale_1.t('Show more')} <icons_1.IconAdd isCircled size="md"/>
                </react_1.Fragment>)}
            </ExpandButton>)}
        </styles_1.CauseHeader>
        <panels_1.Panel>
          {commits.slice(0, expanded ? 100 : 1).map(function (commit) { return (<commitRow_1.default key={commit.id} commit={commit}/>); })}
        </panels_1.Panel>
      </styles_1.DataSection>);
    };
    return EventCause;
}(react_1.Component));
var ExpandButton = styled_1.default('button')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  & > svg {\n    margin-left: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  & > svg {\n    margin-left: ", ";\n  }\n"])), space_1.default(0.5));
exports.default = withApi_1.default(withCommitters_1.default(EventCause));
var templateObject_1;
//# sourceMappingURL=eventCause.jsx.map