Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var modal_1 = require("sentry-test/modal");
var modal_2 = require("app/actionCreators/modal");
var modalActions_1 = tslib_1.__importDefault(require("app/actions/modalActions"));
// @ts-expect-error
var group = TestStubs.Group({
    id: '1337',
    pluginActions: [],
    pluginIssues: [],
});
// @ts-expect-error
var organization = TestStubs.Organization({
    id: '4660',
    slug: 'org',
    features: ['reprocessing-v2'],
});
function renderComponent() {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var modal;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, modal_1.mountGlobalModal()];
                case 1:
                    modal = _a.sent();
                    modal_2.openReprocessEventModal({ organization: organization, groupId: group.id });
                    // @ts-expect-error
                    return [4 /*yield*/, tick()];
                case 2:
                    // @ts-expect-error
                    _a.sent();
                    // @ts-expect-error
                    return [4 /*yield*/, tick()];
                case 3:
                    // @ts-expect-error
                    _a.sent();
                    modal.update();
                    return [2 /*return*/, modal];
            }
        });
    });
}
describe('ReprocessEventModal', function () {
    var _this = this;
    var wrapper;
    beforeAll(function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, renderComponent()];
                    case 1:
                        wrapper = _a.sent();
                        return [2 /*return*/];
                }
            });
        });
    });
    it('modal is open', function () {
        expect(wrapper.find('Header').text()).toEqual('Reprocess Events');
    });
    it('form fields & info', function () {
        // some info about reprocessing
        var introduction = wrapper.find('Introduction');
        expect(introduction).toBeTruthy();
        expect(introduction).toHaveLength(2);
        // Reprocess impacts
        expect(introduction.at(0).text()).toEqual('Reprocessing applies new debug files and grouping enhancements to this Issue. Please consider these impacts:');
        var impacts = wrapper.find('StyledList');
        expect(impacts).toBeTruthy();
        expect(impacts.length).toBeGreaterThan(0);
        // Docs info
        expect(introduction.at(1).text()).toEqual('For more information, please refer to the documentation.');
        // Form
        var form = wrapper.find('Form');
        expect(form).toBeTruthy();
        // Number of events to be reprocessed field
        var reprocessQuantityField = form.find('NumberField');
        expect(reprocessQuantityField).toBeTruthy();
        // Remaining events action field
        var remainingEventsActionField = form.find('RadioField');
        expect(remainingEventsActionField).toBeTruthy();
    });
    it('reprocess all events', function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
        var closeModalFunc, reprocessQuantityField, submitButton;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    // @ts-expect-error
                    MockApiClient.addMockResponse({
                        url: "/organizations/" + organization.slug + "/issues/" + group.id + "/reprocessing/",
                        method: 'POST',
                        body: [],
                    });
                    jest.spyOn(window.location, 'reload').mockImplementation(function () { });
                    closeModalFunc = jest.spyOn(modalActions_1.default, 'closeModal');
                    reprocessQuantityField = wrapper.find('NumberField input');
                    expect(reprocessQuantityField.props().placeholder).toEqual('Reprocess all events');
                    expect(reprocessQuantityField.props().value).toEqual(undefined);
                    submitButton = wrapper.find('[data-test-id="form-submit"]').hostNodes();
                    submitButton.simulate('submit');
                    // @ts-expect-error
                    return [4 /*yield*/, tick()];
                case 1:
                    // @ts-expect-error
                    _a.sent();
                    wrapper.update();
                    expect(window.location.reload).toHaveBeenCalled();
                    expect(closeModalFunc).toHaveBeenCalled();
                    return [2 /*return*/];
            }
        });
    }); });
});
//# sourceMappingURL=reprocessEventModal.spec.jsx.map