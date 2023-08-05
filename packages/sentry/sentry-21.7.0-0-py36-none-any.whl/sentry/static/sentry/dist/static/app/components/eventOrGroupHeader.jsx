Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var react_2 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var capitalize_1 = tslib_1.__importDefault(require("lodash/capitalize"));
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var eventOrGroupTitle_1 = tslib_1.__importDefault(require("app/components/eventOrGroupTitle"));
var globalSelectionLink_1 = tslib_1.__importDefault(require("app/components/globalSelectionLink"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var events_1 = require("app/utils/events");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var unhandledTag_1 = require("app/views/organizationGroupDetails/unhandledTag");
var eventTitleError_1 = tslib_1.__importDefault(require("./eventTitleError"));
/**
 * Displays an event or group/issue title (i.e. in Stream)
 */
var EventOrGroupHeader = /** @class */ (function (_super) {
    tslib_1.__extends(EventOrGroupHeader, _super);
    function EventOrGroupHeader() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EventOrGroupHeader.prototype.getTitleChildren = function () {
        var _a;
        var _b = this.props, hideIcons = _b.hideIcons, hideLevel = _b.hideLevel, data = _b.data, index = _b.index, organization = _b.organization;
        var _c = data, level = _c.level, status = _c.status, isBookmarked = _c.isBookmarked, hasSeen = _c.hasSeen;
        var hasGroupingTreeUI = !!((_a = organization.features) === null || _a === void 0 ? void 0 : _a.includes('grouping-tree-ui'));
        return (<react_1.Fragment>
        {!hideLevel && level && (<GroupLevel level={level}>
            <tooltip_1.default title={"Error level: " + capitalize_1.default(level)}>
              <span />
            </tooltip_1.default>
          </GroupLevel>)}
        {!hideIcons && status === 'ignored' && (<IconWrapper>
            <icons_1.IconMute color="red300"/>
          </IconWrapper>)}
        {!hideIcons && isBookmarked && (<IconWrapper>
            <icons_1.IconStar isSolid color="yellow300"/>
          </IconWrapper>)}

        <errorBoundary_1.default customComponent={<eventTitleError_1.default />} mini>
          <StyledEventOrGroupTitle {...this.props} hasSeen={hasGroupingTreeUI && hasSeen === undefined ? true : hasSeen} withStackTracePreview hasGuideAnchor={index === 0} guideAnchorName="issue_stream_title"/>
        </errorBoundary_1.default>
      </react_1.Fragment>);
    };
    EventOrGroupHeader.prototype.getTitle = function () {
        var _a = this.props, includeLink = _a.includeLink, data = _a.data, params = _a.params, location = _a.location, onClick = _a.onClick;
        var orgId = params === null || params === void 0 ? void 0 : params.orgId;
        var _b = data, id = _b.id, status = _b.status;
        var _c = data, eventID = _c.eventID, groupID = _c.groupID;
        var props = {
            'data-test-id': status === 'resolved' ? 'resolved-issue' : null,
            style: status === 'resolved' ? { textDecoration: 'line-through' } : undefined,
        };
        if (includeLink) {
            return (<globalSelectionLink_1.default {...props} to={{
                    pathname: "/organizations/" + orgId + "/issues/" + (eventID ? groupID : id) + "/" + (eventID ? "events/" + eventID + "/" : ''),
                    query: tslib_1.__assign(tslib_1.__assign({ query: this.props.query }, (location.query.sort !== undefined ? { sort: location.query.sort } : {})), (location.query.project !== undefined ? {} : { _allp: 1 })),
                }} onClick={onClick}>
          {this.getTitleChildren()}
        </globalSelectionLink_1.default>);
        }
        else {
            return <span {...props}>{this.getTitleChildren()}</span>;
        }
    };
    EventOrGroupHeader.prototype.render = function () {
        var _a = this.props, className = _a.className, size = _a.size, data = _a.data;
        var location = events_1.getLocation(data);
        var message = events_1.getMessage(data);
        return (<div className={className} data-test-id="event-issue-header">
        <Title size={size}>{this.getTitle()}</Title>
        {location && <Location size={size}>{location}</Location>}
        {message && (<StyledTagAndMessageWrapper size={size}>
            {message && <Message>{message}</Message>}
          </StyledTagAndMessageWrapper>)}
      </div>);
    };
    EventOrGroupHeader.defaultProps = {
        includeLink: true,
        size: 'normal',
    };
    return EventOrGroupHeader;
}(react_1.Component));
var truncateStyles = react_2.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  overflow: hidden;\n  max-width: 100%;\n  text-overflow: ellipsis;\n  white-space: nowrap;\n"], ["\n  overflow: hidden;\n  max-width: 100%;\n  text-overflow: ellipsis;\n  white-space: nowrap;\n"])));
var getMargin = function (_a) {
    var size = _a.size;
    if (size === 'small') {
        return 'margin: 0;';
    }
    return 'margin: 0 0 5px';
};
var Title = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  ", ";\n  line-height: 1;\n  ", ";\n  & em {\n    font-size: ", ";\n    font-style: normal;\n    font-weight: 300;\n    color: ", ";\n  }\n"], ["\n  ", ";\n  line-height: 1;\n  ", ";\n  & em {\n    font-size: ", ";\n    font-style: normal;\n    font-weight: 300;\n    color: ", ";\n  }\n"])), truncateStyles, getMargin, function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.subText; });
var LocationWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  ", ";\n  ", ";\n  direction: rtl;\n  text-align: left;\n  font-size: ", ";\n  color: ", ";\n  span {\n    direction: ltr;\n  }\n"], ["\n  ", ";\n  ", ";\n  direction: rtl;\n  text-align: left;\n  font-size: ", ";\n  color: ", ";\n  span {\n    direction: ltr;\n  }\n"])), truncateStyles, getMargin, function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.subText; });
function Location(props) {
    var children = props.children, rest = tslib_1.__rest(props, ["children"]);
    return (<LocationWrapper {...rest}>
      {locale_1.tct('in [location]', {
            location: <span>{children}</span>,
        })}
    </LocationWrapper>);
}
var StyledTagAndMessageWrapper = styled_1.default(unhandledTag_1.TagAndMessageWrapper)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), getMargin);
var Message = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  ", ";\n  font-size: ", ";\n"], ["\n  ", ";\n  font-size: ", ";\n"])), truncateStyles, function (p) { return p.theme.fontSizeMedium; });
var IconWrapper = styled_1.default('span')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  top: 2px;\n\n  margin-right: 5px;\n"], ["\n  position: relative;\n  top: 2px;\n\n  margin-right: 5px;\n"])));
var GroupLevel = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  left: -1px;\n  width: 9px;\n  height: 15px;\n  border-radius: 0 3px 3px 0;\n\n  background-color: ", ";\n\n  & span {\n    display: block;\n    width: 9px;\n    height: 15px;\n  }\n"], ["\n  position: absolute;\n  left: -1px;\n  width: 9px;\n  height: 15px;\n  border-radius: 0 3px 3px 0;\n\n  background-color: ", ";\n\n  & span {\n    display: block;\n    width: 9px;\n    height: 15px;\n  }\n"])), function (p) { var _a; return (_a = p.theme.level[p.level]) !== null && _a !== void 0 ? _a : p.theme.level.default; });
exports.default = react_router_1.withRouter(withOrganization_1.default(EventOrGroupHeader));
var StyledEventOrGroupTitle = styled_1.default(eventOrGroupTitle_1.default)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  font-weight: ", ";\n"], ["\n  font-weight: ", ";\n"])), function (p) { return (p.hasSeen ? 400 : 600); });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=eventOrGroupHeader.jsx.map