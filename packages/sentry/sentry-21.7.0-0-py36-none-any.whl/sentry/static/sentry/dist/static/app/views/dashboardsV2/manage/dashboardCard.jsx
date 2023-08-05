Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var avatar_1 = tslib_1.__importDefault(require("app/components/activity/item/avatar"));
var card_1 = tslib_1.__importDefault(require("app/components/card"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function DashboardCard(_a) {
    var title = _a.title, detail = _a.detail, createdBy = _a.createdBy, renderWidgets = _a.renderWidgets, dateStatus = _a.dateStatus, to = _a.to, onEventClick = _a.onEventClick, renderContextMenu = _a.renderContextMenu;
    function onClick() {
        onEventClick === null || onEventClick === void 0 ? void 0 : onEventClick();
    }
    return (<link_1.default data-test-id={"card-" + title} onClick={onClick} to={to}>
      <StyledDashboardCard interactive>
        <CardHeader>
          <CardContent>
            <Title>{title}</Title>
            <Detail>{detail}</Detail>
          </CardContent>
          <AvatarWrapper>
            {createdBy ? (<avatar_1.default type="user" user={createdBy} size={34}/>) : (<avatar_1.default type="system" size={34}/>)}
          </AvatarWrapper>
        </CardHeader>
        <CardBody>{renderWidgets()}</CardBody>
        <CardFooter>
          <DateSelected>
            {dateStatus ? (<DateStatus>
                {locale_1.t('Created')} {dateStatus}
              </DateStatus>) : (<DateStatus />)}
          </DateSelected>
          {renderContextMenu && renderContextMenu()}
        </CardFooter>
      </StyledDashboardCard>
    </link_1.default>);
}
var AvatarWrapper = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  border: 3px solid ", ";\n  border-radius: 50%;\n  height: min-content;\n"], ["\n  border: 3px solid ", ";\n  border-radius: 50%;\n  height: min-content;\n"])), function (p) { return p.theme.border; });
var CardContent = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  flex-grow: 1;\n  overflow: hidden;\n  margin-right: ", ";\n"], ["\n  flex-grow: 1;\n  overflow: hidden;\n  margin-right: ", ";\n"])), space_1.default(1));
var StyledDashboardCard = styled_1.default(card_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  justify-content: space-between;\n  height: 100%;\n  &:focus,\n  &:hover {\n    top: -1px;\n  }\n"], ["\n  justify-content: space-between;\n  height: 100%;\n  &:focus,\n  &:hover {\n    top: -1px;\n  }\n"])));
var CardHeader = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  padding: ", " ", ";\n"], ["\n  display: flex;\n  padding: ", " ", ";\n"])), space_1.default(1.5), space_1.default(2));
var Title = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  ", ";\n"], ["\n  color: ", ";\n  ", ";\n"])), function (p) { return p.theme.textColor; }, overflowEllipsis_1.default);
var Detail = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  font-family: ", ";\n  font-size: ", ";\n  color: ", ";\n  ", ";\n  line-height: 1.5;\n"], ["\n  font-family: ", ";\n  font-size: ", ";\n  color: ", ";\n  ", ";\n  line-height: 1.5;\n"])), function (p) { return p.theme.text.familyMono; }, function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray300; }, overflowEllipsis_1.default);
var CardBody = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  background: ", ";\n  padding: ", " ", ";\n  max-height: 150px;\n  min-height: 150px;\n  overflow: hidden;\n"], ["\n  background: ", ";\n  padding: ", " ", ";\n  max-height: 150px;\n  min-height: 150px;\n  overflow: hidden;\n"])), function (p) { return p.theme.gray100; }, space_1.default(1.5), space_1.default(2));
var CardFooter = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  padding: ", " ", ";\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  padding: ", " ", ";\n"])), space_1.default(1), space_1.default(2));
var DateSelected = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  display: grid;\n  grid-column-gap: ", ";\n  color: ", ";\n  ", ";\n"], ["\n  font-size: ", ";\n  display: grid;\n  grid-column-gap: ", ";\n  color: ", ";\n  ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, space_1.default(1), function (p) { return p.theme.textColor; }, overflowEllipsis_1.default);
var DateStatus = styled_1.default('span')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  padding-left: ", ";\n"], ["\n  color: ", ";\n  padding-left: ", ";\n"])), function (p) { return p.theme.purple300; }, space_1.default(1));
exports.default = DashboardCard;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=dashboardCard.jsx.map